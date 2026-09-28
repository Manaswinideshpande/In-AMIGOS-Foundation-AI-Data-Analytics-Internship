"""
NGO / Fellowship opportunity scraper — 15 organizations, corrected version.
General fixes applied throughout vs. the draft notes:
- soup.select() needs ONE dotted compound selector for multi-class matches
  (e.g. "h3.a.b.c"), not space-separated class names (space = descendant selector).
- Tailwind-style utility class chains (with ':' or '[...]') are invalid CSS as
  literal class names and are fragile even escaped, since they regenerate on
  rebuilds -> replaced with keyword text-scans over a small set of tags instead.
- soup.select('a.href') does not select by the href ATTRIBUTE - '.href' was being
  read as a class name -> fixed to a[href*='...'] or a direct fallback URL.
- Free-text notes ("currently closed", "on hold", "email to apply") are not code
  -> converted into literal fallback strings, flagged with TODO where you should
  reconfirm against the live page.
- Organizations with multiple distinct opportunities (Goonj, CRY) collect all of
  them and join into one string, so the final table stays at one row per org.

IMPORTANT: I do not have live internet access in this environment, so none of
these selectors have been run against the actual current HTML. Treat every
`# TODO` / `# CONFIRM` comment as something to verify yourself before relying
on the output.
"""
import urllib.request
import urllib.parse
# or


from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
TIMEOUT = 15
all_records = []


def safe_get(url):
    """GET a URL with headers/timeout, returning a BeautifulSoup object or None."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code != 200:
            print(f"[WARN] {url} returned status {resp.status_code}")
            return None
        return BeautifulSoup(resp.content, "html.parser")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def first_text_containing(soup, tags, keyword, max_len=80):
    """Scan a small set of tag names, return first text containing keyword (case-insensitive)."""
    if not soup:
        return None
    for tag in soup.find_all(tags):
        text = tag.get_text(strip=True)
        if keyword.lower() in text.lower() and 0 < len(text) <= max_len:
            return text
    return None


# ==========================================
# 1. Teach For India
# ==========================================
soup = safe_get("https://www.teachforindia.org/")
Organization_Name = "Teach For India"
if soup:
    for tag in soup.select("h2.heading-h2.white-text.margin-top"):
        t = tag.get_text(strip=True)
        if "Teach For India" in t:
            Organization_Name = t.split(",")[0].strip()
            break
Opportunity_Name = "Fellowship"
if soup:
    for tag in soup.select("div.text-block-18"):
        t = tag.get_text(strip=True)
        if "Fellowship" in t:
            Opportunity_Name = t
            break
all_records.append({
    "Organization_Name": Organization_Name,
    "Opportunity_Name": Opportunity_Name,
    "Application_Deadline": "NA",
    "Application_Link": urljoin("https://apply.teachforindia.org", "/signup"),
})

# ==========================================
# 2. iVolunteer
# ==========================================
soup1 = safe_get("https://www.ivolunteer.in")
Organization_Name = "iVolunteer"
if soup1:
    for tag in soup1.select("div.headerimage.full-width"):
        t = tag.get_text(strip=True)
        if "iVolunteer" in t:
            Organization_Name = t.split(",")[0].strip()
            break
Opportunity_Name = "Volunteer / India Fellow"
if soup1:
    for tag in soup1.find_all(["div", "h2", "a"]):
        t = tag.get_text(strip=True)
        if "volunteer" in t.lower() or "india fellow" in t.lower():
            extracted = t.split(",")[0].strip()
            if 0 < len(extracted) < 100:
                Opportunity_Name = extracted
                break
all_records.append({
    "Organization_Name": Organization_Name,
    "Opportunity_Name": Opportunity_Name,
    "Application_Deadline": "NA",
    "Application_Link": "https://www.ivolunteer.in",
})

# ==========================================
# 3. Make A Difference (MAD)
# ==========================================
base_url_mad = "https://www.makeadiff.in"
soup_mad = safe_get(base_url_mad)
org_name_mad = "Make A Difference"
opportunity_name_mad = "Volunteer / Youth Mentorship"
app_link_mad = "https://www.makeadiff.in/volunteer"
if soup_mad:
    tag = soup_mad.select_one("h6.center-align")
    if tag:
        org_name_mad = tag.get_text(strip=True).split('•')[0].strip()
    tag = soup_mad.select_one("a.secondary-button.yellow-fill.w-button")
    if tag:
        opportunity_name_mad = tag.get_text(strip=True)
    menu_stack = soup_mad.select_one("div.application-process-header.p-0")
    if menu_stack:
        link_tag = menu_stack.select_one("a.secondary-button")
        if link_tag and link_tag.get("href"):
            app_link_mad = urljoin(base_url_mad, link_tag["href"])
all_records.append({
    "Organization_Name": org_name_mad,
    "Opportunity_Name": opportunity_name_mad,
    "Application_Deadline": "NA",
    "Application_Link": app_link_mad,
})

# ==========================================
# 4. Pratham
# ==========================================
soup3 = safe_get("https://www.pratham.org/")
Organization_Name = "Pratham"
if soup3:
    for tag in soup3.select("div.head-left"):
        t = tag.get_text(strip=True)
        if "pratham" in t.lower():
            Organization_Name = t.split(",")[0].strip()
            break
all_records.append({
    "Organization_Name": Organization_Name,
    "Opportunity_Name": "Volunteer / Fellowship",
    "Application_Deadline": "NA",
    "Application_Link": "https://www.pratham.org/",
})

# ==========================================
# 5. Gandhi Fellowship (Piramal Foundation)
# ==========================================
soup5 = safe_get("https://gandhifellowship.org/initiatives/")
org_name_gf = "Piramal Foundation - Gandhi Fellowship"
found = first_text_containing(soup5, "span", "piramal", max_len=60)
if found:
    org_name_gf = found
opportunity_gf = "Gandhi Fellowship"
if soup5:
    # FIX: original selector had a stray double space between classes
    # ("style-default  highlight-default") -> joined into one dotted selector
    tag = soup5.select_one("h3.pxl-item--title.style-default.highlight-default")
    if tag and tag.get_text(strip=True):
        opportunity_gf = tag.get_text(strip=True)
all_records.append({
    "Organization_Name": org_name_gf,
    "Opportunity_Name": opportunity_gf,
    "Application_Deadline": "NA",
    "Application_Link": "NA",  # TODO: you flagged you couldn't locate this - confirm manually
})

# ==========================================
# 6. SBI Youth for India Fellowship
# ==========================================
soup6 = safe_get("https://www.youthforindia.org/")
org_name_sbi = "SBI Youth for India Fellowship"
# FIX: original selector chained Tailwind utility classes with ':' (e.g. md:text-2xl)
# directly as class names -> invalid CSS. Using a keyword text-scan instead.
found = first_text_containing(soup6, ["div", "h1", "h2"], "youth for india", max_len=80)
if found:
    org_name_sbi = found
opportunity_sbi = "Rural Development Fellowship"
found = first_text_containing(soup6, ["span", "h1", "h2"], "fellowship", max_len=100)
if found:
    opportunity_sbi = found
all_records.append({
    "Organization_Name": org_name_sbi,
    "Opportunity_Name": opportunity_sbi,
    # Per your note: program is paused for this cycle - kept as a literal fallback
    "Application_Deadline": "On hold for Fellowship year 2026-27 (per program notice)",
    "Application_Link": "https://www.youthforindia.org/",  # CONFIRM exact apply URL
})

# ==========================================
# 7. India Fellow
# ==========================================
soup7 = safe_get("https://indiafellow.org/")
org_name_if = "India Fellow"
opportunity_if = "Fellowship"
if soup7:
    tag = soup7.select_one("div.et_pb_text_inner")
    if tag and tag.get_text(strip=True):
        opportunity_if = tag.get_text(strip=True)[:100]
app_link_if = "https://indiafellow.org/apply-now/"
if soup7:
    # FIX: 'a.href' selected by a nonexistent class called "href" -> use an
    # attribute selector on href instead
    link_tag = soup7.select_one("a[href*='apply']")
    if link_tag and link_tag.get("href"):
        app_link_if = urljoin("https://indiafellow.org/", link_tag["href"])
all_records.append({
    "Organization_Name": org_name_if,
    "Opportunity_Name": opportunity_if,
    "Application_Deadline": "Currently closed; expected to reopen in 2027 (per site notice)",
    "Application_Link": app_link_if,
})

# ==========================================
# 8. Bhumi
# ==========================================
soup8 = safe_get("https://www.bhumi.ngo/about-us")
org_name_bhumi = "Bhumi"  # Default fallback name

soup8 = safe_get("https://www.bhumi.ngo/about-us")
org_name_bhumi = "Bhumi"  # Default fallback name

if soup8:
    tag = soup8.select_one("h3.framer-text")
    if tag:
        text_content = tag.get_text(strip=True)
        
        # Option A: If it starts with "Bhumi", just use "Bhumi" explicitly
        if text_content.startswith("Bhumi"):
            org_name_bhumi = "Bhumi"
        else:
            # Option B: Otherwise take the first word/split text safely
            org_name_bhumi = text_content.split()[0].strip()

print(org_name_bhumi)  # Output will be: Bhumi
opportunity_bhumi = "Volunteering with Bhumi"
if soup8:
    tag = soup8.select_one("div.framer-154toym")
    if tag and tag.get_text(strip=True):
        opportunity_bhumi = tag.get_text(strip=True)
all_records.append({
    "Organization_Name": org_name_bhumi,
    "Opportunity_Name": opportunity_bhumi,
    "Application_Deadline": "NA",
    # FIX: 'div.form-all' is a form container, not a link - hardcoded the join page instead
    "Application_Link": "https://www.bhumi.ngo/join-us",  # CONFIRM
})

# ==========================================
# 9. Akanksha Foundation
# ==========================================
soup9 = safe_get("https://akanksha.org/about/vision_mission")
org_name_ak = "Akanksha Foundation"
# FIX: original selector chained Tailwind utility classes including 'hover:opacity-100'
# (invalid CSS without escaping, and fragile even escaped) -> keyword scan instead
found = first_text_containing(soup9, ["p", "span", "div"], "akanksha", max_len=60)
if found:
    org_name_ak = found
all_records.append({
    "Organization_Name": org_name_ak,
    "Opportunity_Name": "Volunteer with Us",
    "Application_Deadline": "NA",
    "Application_Link": "https://akanksha.org/join-us/volunteer-with-us",
})

# ==========================================
# 10. Barefoot College
# ==========================================
soup10 = safe_get("https://www.barefootcollege.org/")
opportunity_bf = "Volunteer / Fellowship"
if soup10:
    # FIX: "h3.elementor-heading-title elementor-size-default" (space) treated the
    # second class as a descendant tag name -> joined into one compound selector
    tags = soup10.select("h3.elementor-heading-title.elementor-size-default")
    texts = [t.get_text(strip=True) for t in tags if t.get_text(strip=True)]
    if texts:
        opportunity_bf = texts[0]
all_records.append({
    "Organization_Name": "Barefoot College",
    "Opportunity_Name": opportunity_bf,
    "Application_Deadline": "NA",
    "Application_Link": "https://www.barefootcollege.org/get-involved/",  # CONFIRM
})

# ==========================================
# 11. Salaam Bombay Foundation
# (No URL/name given in your notes for block #11 - assumed based on our
#  earlier 15-org list. CONFIRM this is the right organization / URL.)
# ==========================================
soup11 = safe_get("https://www.salaambombay.org/")
org_name_sb = "Salaam Bombay Foundation"
if soup11:
    # FIX: joined classes with dots instead of spaces
    tag = soup11.select_one("div.col-sm-12.col-xs-12.col-lg-5.col-md-5")
    if tag and tag.get_text(strip=True):
        org_name_sb = tag.get_text(strip=True)[:60]
opportunity_sb = "Volunteer / Engagement Program"
if soup11:
    tag = soup11.select_one("div.engament_list")
    if tag and tag.get_text(strip=True):
        opportunity_sb = tag.get_text(strip=True)[:100]
app_link_sb = "https://www.salaambombay.org/get-involved"  # CONFIRM
if soup11:
    section = soup11.select_one("section.sectionmanageform")
    if section:
        a = section.find("a", href=True)
        if a:
            app_link_sb = urljoin("https://www.salaambombay.org/", a["href"])
all_records.append({
    "Organization_Name": org_name_sb,
    "Opportunity_Name": opportunity_sb,
    "Application_Deadline": "NA",
    "Application_Link": app_link_sb,
})

# ==========================================
# 12. Habitat for Humanity India
# ==========================================
soup12 = safe_get("https://habitatindia.org/about/")
org_name_hh = "Habitat for Humanity India"
if soup12:
    # FIX: joined classes with dots instead of spaces
    tag = soup12.select_one("p.p2.nomar.padb25")
    if tag and tag.get_text(strip=True):
        org_name_hh = tag.get_text(strip=True)[:26]
opportunity_hh = "Volunteering Program"
if soup12:
    tag = (
        soup12.select_one("h1.h2xs.fw7.nomar.pad20.pagetitle.bg2")
        or soup12.select_one("h1.entry-title")
    )
    if tag and tag.get_text(strip=True):
        opportunity_hh = tag.get_text(strip=True)
all_records.append({
    "Organization_Name": org_name_hh,
    "Opportunity_Name": opportunity_hh,
    "Application_Deadline": "NA",
    # The apply UI is an embedded contact/CSR form (#getintouch), not a plain link
    "Application_Link": "https://habitatindia.org/get-involved/#getintouch",  # CONFIRM
})

# ==========================================
# 13. Goonj (multiple opportunities -> joined into one row)
# ==========================================
soup13 = safe_get("https://goonj.org/")
name_tag = soup13.select_one("header #logo a, a.brand") if soup13 else None
org_name_goonj = name_tag.get_text(strip=True) if name_tag and name_tag.get_text(strip=True) else "Goonj"

soupurl = safe_get("https://goonj.org/get-involved/")

# Keywords that mark a section as NOT a real "opportunity" — donation asks,
# partnership pitches, and contact/email CTAs, not something to "apply" to
EXCLUDE_KEYWORDS = ["donate", "gullak", "partner", "contact", "email-protection"]

opportunities_goonj = []  # list of (name, link) pairs, kept together

if soupurl:
    for h3 in soupurl.select("h3.cmsmasters_heading"):
        text = h3.get_text(strip=True)
        if not text:
            continue

        column = h3.find_parent("div", class_="cmsmasters_column")
        link_tag = column.select_one("a.custom--btn") if column else None
        href = link_tag["href"] if link_tag and link_tag.get("href") else "NA"

        # skip donation/partner/contact CTAs and obfuscated Cloudflare email links
        if any(k in text.lower() for k in EXCLUDE_KEYWORDS) or "email-protection" in href:
            continue

        opportunities_goonj.append((text, href))

# Build the two output fields, name and link now guaranteed to stay paired
Opportunity_Name = "; ".join(name for name, _ in opportunities_goonj) or "Volunteer with Goonj"
Application_Link = "; ".join(href for _, href in opportunities_goonj) or "https://goonj.org/volunteer/"
all_records.append({
    "Organization_Name":org_name_goonj,
    "Opportunity_Name":Opportunity_Name,
    "Application_Deadline": "NA",
    "Application_Link":Application_Link,
})

# ==========================================
# 14. CRY - Child Rights and You
# ==========================================
soup14 = safe_get("https://www.cry.org/")
name_tag = soup14.select_one("a.custom-logo-link, div.site-logo a") if soup14 else None
org_name_cry = name_tag.get_text(strip=True) if name_tag and name_tag.get_text(strip=True) else "Child Rights and You (CRY)"

opportunity_cry = "Volunteer / Intern"
if soup14:
    titles = [t.get_text(strip=True) for t in soup14.select("h3.volunteer-options-title") if t.get_text(strip=True)]
    if titles:
        opportunity_cry = " / ".join(titles)

all_records.append({
    "Organization_Name": org_name_cry,
    "Opportunity_Name": opportunity_cry,
    "Application_Deadline": "NA",
    # Per your note: no self-serve apply link found - application is via email
    "Application_Link": "mailto:writetous@crymail.org",  # CONFIRM this address
})

# ==========================================
# 15. Smile Foundation
# ==========================================
soup15 = safe_get("https://www.smilefoundationindia.org/")
# FIX: original variable was misspelled "ame_tag" -> "name_tag"
name_tag = soup15.select_one("a.navbar-brand, div.logo a") if soup15 else None
org_name_smile = name_tag.get_text(strip=True) if name_tag and name_tag.get_text(strip=True) else "Smile Foundation"

opportunity_smile = "Volunteer"
if soup15:
    for a in soup15.select("li.elementor-icon-list-item a"):
        if a.get_text(strip=True).lower() == "volunteer":
            opportunity_smile = a.get_text(strip=True)
            break

app_link_smile = "https://www.smilefoundationindia.org/volunteer/"
if soup15:
    vol = soup15.find("a", href=lambda h: h and "forms" in h and "viewform" in h)
    if vol and vol.get("href"):
        app_link_smile = vol["href"]

all_records.append({
    "Organization_Name": org_name_smile,
    "Opportunity_Name": opportunity_smile,
    "Application_Deadline": "NA",
    "Application_Link": app_link_smile,
})

# ==========================================
# Final combined output - all 15 organizations
# ==========================================

#df.to_csv("D:/IAF INTERNSHIP/tasks3/excelfile/ngo_opportunities_15.csv", index=False)
#print("Saved combined results to ngo_opportunities_15.csv",)


# Assume your scraped data is stored in all_records
df = pd.DataFrame(all_records)
print(df)
print(f"\nTotal organizations scraped: {len(df)}")

# Define your file path (using .xlsx extension)
excel_path = "D:/IAF INTERNSHIP/tasks3/excelfile/ngo_opportunities_15.xlsx"

# Save to Excel using openpyxl engine (index=False prevents saving the row index numbers)
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"Saved combined results to {excel_path}")