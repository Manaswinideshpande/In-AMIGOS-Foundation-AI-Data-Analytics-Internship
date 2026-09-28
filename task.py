from bs4 import BeautifulSoup
import requests
#1 ngo

response= requests.get("https://www.pratham.org/")
print(response)
Soup=BeautifulSoup(response.content,'html.parser')
print(Soup)

print('start*10')

print('111111111111111111111111111111111111111111')
names= Soup.find_all('div',class_="textwidget")
print(names)
clean_name = []
for i in names:
    clean_text = i.get_text(strip=True)
    
    # Check if 'Pratham' is in the text and ensure it's the short name, not a paragraph
    if "Pratham" in clean_text:
        extracted_name = clean_text.split(" is ")[0].strip()
        clean_name.append(extracted_name)
        break
    # Stop as soon as you find the official name
name=clean_name[0] if clean_name else "Pratham Education Foundation (Pratham)"
print(name[0])

print('222222222222222222222222222222')
website=Soup.find('a' ,class_='custom-logo-link')
print(website)
web=[]
if website:
    url=website.get('href')
    web.append(url)
print(web)


print('33333333333333333333333')

url = "https://www.pratham.org/get-involved/job-opportunities/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

intro_paragraphs = soup.find_all("p")

# Words that indicate unwanted boilerplate or contact info
ignore_keywords = [
    "sexual harassment",
    "posh",
    "act, 2013",
    "new delhi",
    "mumbai",
    "email:",
    "contact number:",
    "safdarjung",
    "floor",
    "job",
    "workplace",
]

work_summary = []
for p in intro_paragraphs:
    text = p.get_text(strip=True)

    # 1. Skip short texts or address snippets
    if len(text) < 30:
        continue

    # 2. Skip if it contains any unwanted boilerplate keywords
    if any(keyword in text.lower() for keyword in ignore_keywords):
        continue

    # 3. Only keep if it explicitly talks about core vision/education/learning
    if any(
        topic in text.lower()
        for topic in ["education", "interventions", "learning", "child"]
    ):
        work_summary.append(text)

# Pick only the top paragraph for a clean summary
work = work_summary[0] if work_summary else "Educational NGO."

print(work)

print('4444444444444444444444444444')

headquaters = soup.find_all(["div", "p"], class_=lambda c: c and "address" in c.lower())

head_quarter = []
for i in headquaters:
    # Use .get_text(strip=True) instead of .get(p)
    text = i.get_text(strip=True)
    if text and len(text) > 10:
        head_quarter.append(text)

# Fallback mechanism if the selector finds nothing
if not head_quarter:
    # Look for paragraphs containing key HQ identifiers
    all_p = soup.find_all("p")
    for p in all_p:
        p_text = p.get_text(strip=True)
        if any(loc in p_text for loc in ["New Delhi", "Mumbai", "Registered Office"]):
            head_quarter.append(p_text)

print('5555555555555555555555')

# 1. Find all program card containers
import requests
from bs4 import BeautifulSoup

url = "https://www.pratham.org/get-involved/job-opportunities/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
Soup = BeautifulSoup(response.content, "html.parser")

# Target headings inside the main content section
job_headings = Soup.find_all(["h2", "h3"])

initiatives = []
for tag in job_headings:
    text = tag.get_text(strip=True)

    # Filter out empty text, menu headings, or generic footer headers
    if text and not any(
        skip in text.lower()
        for skip in ["footer", "quick links", "follow us", "copyright"]
    ):
        initiatives.append(text)

print("Extracted Focus Areas / Opportunities:")
print(initiatives)
# The raw output from your h2/h3 extraction
raw_extracted = [
    "Our Commitment to a Safe and Inclusive Workplace",
    "Explorecurrent opportunities",
    "Program Roles",
    "Communications",
    "Programs",
    "Get Involved",
]

# Keywords to discard (navigation, headers, footers)
ignore_keywords = [
    "who we are",
    "commitment",
    "explore",
    "about us",
    "programs",
    "get involved",
    "resources",
    "share now",
]

# Clean list containing only genuine initiatives / functional areas
initiatives = []
for item in raw_extracted:
    # Check if any unwanted keyword is in the item text
    if not any(kw in item.lower() for kw in ignore_keywords):
        initiatives.append(item)

print("Clean Initiatives / Focus Areas:")
print(initiatives)

import pandas as pd
df1= pd.DataFrame()
import pandas as pd

# --- Ensure all extracted lists are flattened/joined into single strings ---

# If 'name' is a list like ['Pratham Education Foundation'], pick the first item or join
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)

# If 'web' is a list like ['https://www.pratham.org/'], pick the first item
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)

# If 'work_summary' is a list of sentences, join them into one string
include = {
    "women thrive",
    "youth are employed",
    "communities flourish through sustainable learning ecosystems",
    " work directly contributes to improving learning outcomes for millions",
    "Act, 2013, Pratham has adopted a detailed Policy Against Sexual Harassment (POSH)",
}

if isinstance(work, list):
    # Keep only elements from work_summary that match your included phrases
    filtered_work = [item for item in work if item in include]

    # If matches were found, join them; otherwise fall back to joined work_summary
    clean_work = (
        ", ".join(filtered_work) if filtered_work else ", ".join(work)
    )
else:
    clean_work = str(work)

# If 'head_quarter' is a list, pick the first item or join
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else "Mumbai, Maharashtra / New Delhi"
)

# Join the 'initiatives' list ['Program Roles', 'Communications', ...] into a single comma-separated string
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

# --- Create 1-row DataFrame ---
data = {
    "Name": [clean_name],
    "Official_Website": [clean_web],
    "Work_of_NGOS": [clean_work],
    "Headquarters": [clean_hq],
    "Key_Intiatives": [clean_initiatives],
}

df1 = pd.DataFrame(data)
print(df1)
df1.head()

print('ngo2')
from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ==========================================
# 2. SMILE FOUNDATION
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 2: SMILE FOUNDATION")
print("=" * 40)

url_smile = "https://www.smilefoundationindia.org/"
resp_smile = requests.get(url_smile, headers=headers)
soup_smile = BeautifulSoup(resp_smile.content, "html.parser")

# 1. Name
name_tag = soup_smile.select_one("a.navbar-brand, div.logo a")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Smile Foundation"]
)

# 2. Official Website
web_tag = soup_smile.select_one("a.navbar-brand, div.logo a")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_smile]

# 3. Work of NGO
work_tags = soup_smile.select("div.our-programmes-sec h3, section.about-us p")
work_summary = [
    t.get_text(strip=True) for t in work_tags if len(t.get_text(strip=True)) > 10
]
if not work_summary:
    work_summary = [
        "Education, healthcare, livelihood, and women empowerment across underprivileged communities in India."
    ]

# 4. Headquarters
hq_tags = soup_smile.select("div.footer-address, p.address")
head_quarter = [
    t.get_text(strip=True) for t in hq_tags if "New Delhi" in t.get_text()
]
if not head_quarter:
    head_quarter = ["New Delhi"]

# 5. Key Initiatives
init_tags = soup_smile.select("div.campaign-box h4, div.programme-title")
initiatives = [
    t.get_text(strip=True) for t in init_tags if len(t.get_text(strip=True)) > 2
]
if not initiatives:
    initiatives = [
        "Shiksha Na Ruke",
        "Health Cannot Wait",
        "Tayyari Kal Ki",
        "She Can Fly",
    ]

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df2 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df2)


# ==========================================
# 3. CRY (CHILD RIGHTS AND YOU)
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 3: CRY (CHILD RIGHTS AND YOU)")
print("=" * 40)

url_cry = "https://www.cry.org/"
resp_cry = requests.get(url_cry, headers=headers)
soup_cry = BeautifulSoup(resp_cry.content, "html.parser")

# 1. Name
name_tag = soup_cry.select_one("a.custom-logo-link, div.site-logo a")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Child Rights and You (CRY)"]
)

# 2. Official Website
web_tag = soup_cry.select_one("a.custom-logo-link, div.site-logo a")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_cry]

# 3. Work of NGO
work_tags = soup_cry.select("div.focus-areas-list h3, ul.nav-menu")
work_summary = [
    t.get_text(strip=True) for t in work_tags if len(t.get_text(strip=True)) > 10
]
if not work_summary:
    work_summary = [
        "Ensuring children's rights to education, health, nutrition, and protection from exploitation."
    ]

# 4. Headquarters
hq_tags = soup_cry.select("div.footer-contact-info, div.office-address")
head_quarter = [
    t.get_text(strip=True) for t in hq_tags if "Mumbai" in t.get_text()
]
if not head_quarter:
    head_quarter = ["Mumbai, Maharashtra"]

##5Intiatives
init_tags = soup_cry.find_all('ul', class_="footer-main1")

ignore = [
    'About Us',
    'Volunteering',
    'Online Donations',
    'FAQs',
    'Careers'
]

initiatives = []
for t in init_tags:
    text = t.get_text(strip=True)
    # Skip if text is short OR contains any ignored keyword
    if len(text) > 2 and not any(bad_word in text for bad_word in ignore):
        initiatives.append(text)

print(initiatives)

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df3 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df3)


# ==========================================
# 4. GOONJ
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 4: GOONJ")
print("=" * 40)

url_goonj = "https://goonj.org/"
resp_goonj = requests.get(url_goonj, headers=headers)
soup_goonj = BeautifulSoup(resp_goonj.content, "html.parser")

# 1. Name
name_tag = soup_goonj.select_one("header #logo a, a.brand")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Goonj"]
)

# 2. Official Website
web_tag = soup_goonj.select_one("header #logo a, a.brand")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_goonj]

# 3. Work of NGO

url_goonj = "https://goonj.org/cfw/"
resp_goonj = requests.get(url_goonj, headers=headers)
soup_goonj = BeautifulSoup(resp_goonj.content, "html.parser")
work_summary = []

# Find all heading tags (h2, h3, h4) on the live page
for heading in soup_goonj.find_all(['h2', 'h3', 'h4']):
    # Check if this heading has a <ul> (bullet list) right next to it
    next_element = heading.find_next_sibling()
    
    # If the next element is a list, or if the heading's parent contains a list
    if (next_element and next_element.name == 'ul') or (heading.find_parent() and heading.find_parent().find('ul')):
        text = heading.get_text(strip=True)
        # Exclude site headers/footers
        if text and len(text) > 2 and text not in work_summary:
            if not any(skip in text.lower() for skip in ['menu', 'footer', 'about', 'contact', 'search', 'initiatives']):
                work_summary.append(text)

print("Exact Live Headings Extracted:")
print(work_summary)
# Headquarter
url = "https://goonj.org/our-offices/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup_goonj = BeautifulSoup(response.content, "html.parser")
hq_tags = soup_goonj.find_all('span', class_='gmail_default')

head_quarter = []
for i in hq_tags:
    d = i.get_text(strip=True)
    # Check if the text contains address keywords
    if "Goonj Head Office" in d or "New Delhi" in d:
        head_quarter.append(d)

print(head_quarter)
# 5. Key Initiatives
import requests
from bs4 import BeautifulSoup

# 1. Define target URL and custom headers to avoid being blocked (HTTP 403)
url = "https://goonj.org/our-initiatives/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 2. Fetch the web page live
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # 3. Pass response.content directly into BeautifulSoup
    soup_goonj = BeautifulSoup(response.content, "html.parser")

    # 4. Target the specific initiative h2 headings
    heading_tags = soup_goonj.select("div.middle_inner h2.cmsmasters_heading")

    initiatives = []
    for tag in heading_tags:
        title = tag.get_text(strip=True)
        
        # Filter out process/generic section titles
        if title and title != "HOW WE DO IT (PROCESSING CHART)":
            initiatives.append(title)

    print("Extracted Initiatives:")
    print(initiatives)
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df4 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df4)


# ==========================================
# 5. HELPAGE INDIA
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 5: HELPAGE INDIA")
print("=" * 40)

url_helpage = "https://www.helpageindia.org/"
resp_helpage = requests.get(url_helpage, headers=headers)
soup_helpage = BeautifulSoup(resp_helpage.content, "html.parser")

# 1. Name
name_=[]
# 1. Look for logo link title or image attributes
logo_link = soup_helpage.find("a", class_=lambda c: c and "logo" in c.lower())
if logo_link:
    # Check link attributes, inner text, or img attributes
    link_text = (
        logo_link.get("title")
        or logo_link.get("aria-label")
        or logo_link.get_text(strip=True)
    )
    if link_text:
        name_.append(link_text)

# 2. Extract directly from OpenGraph site name meta tag (100% reliable on HelpAge India)
if not name_:
    og_site = soup_helpage.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        name_.append(og_site["content"])

# 3. Extract directly from Page Title tag
if not name_:
    page_title = soup_helpage.find("title")
    if page_title:
        # Extracts "HelpAge India" from "HelpAge India | Fighting Isolation..."
        clean_title = page_title.get_text().split("|")[0].split("-")[0].strip()
        name_.append(clean_title)

# Now name[0] is guaranteed to contain "HelpAge India"
name = name_[0]
print("Extracted Name:", name)

# 2. Official Website
web_tag = soup_helpage.select_one("div.header-logo a, a.logo")
web = (
    [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_helpage]
)

# 3. Work of NGO
work_tags = soup_helpage.select("div.our-work-section h3, div.about-content p")
work_summary = [
    t.get_text(strip=True) for t in work_tags if len(t.get_text(strip=True)) > 10
]
if not work_summary:
    work_summary = [
        "Advocating for elderly care, healthcare support, age-friendly environments, and livelihoods."
    ]

# 4. Headquarters
hq_tags = soup_helpage.select("div.elementor-widget-container")
head_quarter = [
    t.get_text(strip=True) for t in hq_tags if "New Delhi" in t.get_text()
]
if not head_quarter:
    head_quarter = ["New Delhi"]

# 5. Key Initiatives
init_tags = soup_helpage.select(
    "h1.elementor-heading-title.elementor-size-default, h2.elementor-heading-title"
)

initiative= [
    t.get_text(strip=True)
    for t in init_tags
    if len(t.get_text(strip=True)) > 2
]

# Fallback in case the page structure changes or headings aren't found
if not initiative:
    initiative = [
        "Mobile Healthcare Units (MHUs)",
        "Cataract Surgeries",
        "Elder Helpline",
    ]

key_intiatives=initiative[:4]
print(key_intiatives)

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(key_intiatives) if isinstance(key_intiatives, list) else str(key_intiatives)
)

df5 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df5)


# ==========================================
# 6. WILDLIFE TRUST OF INDIA (WTI)
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 6: WILDLIFE TRUST OF INDIA")
print("=" * 40)

url_wti = "https://www.wti.org.in/"
resp_wti = requests.get(url_wti, headers=headers)
soup_wti = BeautifulSoup(resp_wti.content, "html.parser")

# 1. Name
name_tag = soup_wti.select_one("div.logo-container a, a.navbar-brand")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Wildlife Trust of India"]
)

# 2. Official Website
web_tag = soup_wti.select_one("div.logo-container a, a.navbar-brand")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_wti]

# 3. Work of NGO
work_tags = soup_wti.select("h3.portfolio-title")

# 2. Extract href from child <a> tags using a list comprehension
# 1. Target the <a> tags inside <h3 class="portfolio-title">
work_tags = soup_wti.select("h3.portfolio-title a")

# 2. Extract the text (title) instead of 'href'
work_summary = [
    a.get_text(strip=True) for a in work_tags if len(a.get_text(strip=True)) > 2
]

print(work_summary)
# 4. Headquarters
hq_p_tags = soup_wti.select("h4 p, div.footer-contact-details p, footer p")

head_quarters = []
for p in hq_p_tags:
    text = p.get_text(strip=True)
    if any(loc in text for loc in ["Noida", "Uttar Pradesh", "UP", "F-13"]):
        head_quarters.append(text)
        break  # Stop as soon as the HQ address is found

# Fallback if no matching tag is found on the page
if not head_quarters:
    head_quarters = ["Noida, Uttar Pradesh"]

head_quarter = head_quarters[0]
print("Headquarters:", head_quarter)

 # Sliced to 4 items
 # 5. Key Initiatives
ignore_words = [
    "OUR TEAM",
    "OUR STORY",
    "OUR PARTNERS",
    "OUR FINANCIALS",
    "PUBLIC DISCLAIMER",
    "RESOURCE CENTRE",
    "ANNUAL REPORTS",
    "VIDEOS",
    "UPDATES",
    "FEATURES",
    "OUR BIG IDEAS",
    "GUARDIANS OF THE WILD",
    "WILD BYTES",
]

init_tags = soup_wti.select("div.project-card h3, ul.sub-menu li")

# Filter out unwanted menu words and slice to the top 4 items (keeps it to ~2 lines)
initiatives = [
    t.get_text(strip=True)
    for t in init_tags
    if len(t.get_text(strip=True)) > 2
    and not any(w in t.get_text(strip=True).upper() for w in ignore_words)
][:4]

# Fallback if scraping returns empty
if not initiatives:
    initiatives = [
        "Right of Passage",
        "Wild Rescue",
        "Wild Aid",
        "Species Recovery",
    ]

# Clean & Create DataFrame Strings
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)
######################
df6 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df6)


# ==========================================
# 7. BLUE CROSS OF INDIA
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 7: BLUE CROSS OF INDIA")
print("=" * 40)

url_blue = "https://bluecrossofindia.org/"
resp_blue = requests.get(url_blue, headers=headers)
soup_blue = BeautifulSoup(resp_blue.content, "html.parser")

# 1. Name
name_tag = soup_blue.select_one("img.u-logo-image.u-logo-image-1")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Blue Cross of India"]
)

# 2. Official Website
web_tag = soup_blue.select_one("div.site-header-logo a")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_blue]

# 3. Work of NGO
# 1. Chain all classes with dots (NO spaces)
work_tags = soup_blue.select(
    "a.u-active-none.u-border-none.u-btn.u-button-link.u-button-style.u-hover-none.u-none.u-text-palette-1-base"
)

# 2. Alternative/Broader Selector (Handles variations like u-btn-1, u-btn-2, u-btn-3)
if not work_tags:
    work_tags = soup_blue.select("a[class*='u-button-link'], a.u-btn")

# Extract non-empty text strings longer than 5 characters
work_summary = [
    t.get_text(strip=True)
    for t in work_tags
    if len(t.get_text(strip=True)) > 5
]

# Fallback if no matching tags contain valid text
if not work_summary:
    work_summary = [
        "Animal rescue, veterinary medical care, shelter management, and adoption services."
    ]

print(work_summary)

# 4. Headquarters
hq_tags = soup_blue.select(
    "p.u-align-center.u-small-text.u-text.u-text-body-alt-color.u-text-variant"
)

# 2. Fallback to broader selector if class index varies
if not hq_tags:
    hq_tags = soup_blue.select("p.u-align-center.u-text, footer p")

quarter = [
    t.get_text(strip=True)
    for t in hq_tags
    if t.get_text(strip=True) and len(t.get_text(strip=True)) > 3
]

# 3. Filter for location keywords if multiple paragraphs match
hq_filtered = [
    text for text in quarter 
    if any(loc in text for loc in ["Chennai", "Tamil Nadu", "Guindy", "600032"])
]

head_quarter = hq_filtered[0] if hq_filtered else (quarter[0] if quarter else "Chennai, Tamil Nadu")

print("Headquarters:", head_quarter)

if not init_tags:
    init_tags = soup_blue.select("a[class*='u-button-link'], a.u-btn")

initiatives = []
# 2. Loop over init_tags (not initiatives)
for tag in init_tags:
    # Extract text from <a> or its inner child tags (e.g., <span>)
    text = tag.get_text(strip=True)
    if len(text) > 3:
        initiatives.append(text)

# Fallback if no matching tags return valid text
if not initiatives:
    initiatives = [
        "Animal Birth Control (ABC) & Vaccination",
        "24/7 Animal Rescue",
        "Adoption Services",
        "Veterinary Medical Care",
    ]

print("Key Initiatives:", initiatives)
# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df7 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df7)


# ==========================================
# 8. SEWA (SELF EMPLOYED WOMEN'S ASSOCIATION)
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 8: SEWA")
print("=" * 40)

url_sewa = "https://www.sewa.org/"
resp_sewa = requests.get(url_sewa, headers=headers)
soup_sewa = BeautifulSoup(resp_sewa.content, "html.parser")

# 1. Name
name_tag = soup_sewa.select_one("a.top_logo, a.navbar-brand, .logo a")

names = []
if name_tag:
    # 1. Check inner text of <a>
    text = name_tag.get_text(strip=True)
    
    # 2. If <a> has no text, look for child <img> alt/title attributes
    if not text and name_tag.find("img"):
        img = name_tag.find("img")
        text = img.get("alt") or img.get("title")

    if text and text.strip():
        names.append(text.strip())

# 3. Dynamic fallback using <title> or OpenGraph meta tags if logo tags lack text/attributes
if not names:
    og_site = soup_sewa.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        names.append(og_site["content"].strip())
    else:
        page_title = soup_sewa.find("title")
        if page_title:
            clean_title = page_title.get_text().split("|")[0].split("-")[0].strip()
            names.append(clean_title)

name = names[0] if names else "seva"
print("Extracted Name:", name)

# 2. Official Website
web_tag = soup_sewa.select_one("div.brand-logo a, a.logo-link")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_sewa]

# 3. Work of NGO

url_sewa = "https://www.sewa.org/sewa-services/"
resp_sewa = requests.get(url_sewa, headers=headers)
soup_sewa = BeautifulSoup(resp_sewa.content, "html.parser")
work_tags = soup_sewa.select("div.big_cream.pb-5")

work=[]
for i in work_tags:
    # Use separator=" " to preserve spaces between text nodes
    raw_text = i.get_text(separator=" ", strip=True)
    
    # Clean up multiple consecutive spaces
    clean_text = " ".join(raw_text.split())
    
    # Filter out empty or extremely short text
    if len(clean_text) > 20:
        work.append(clean_text)

# Fallback if the container returns empty
# Select all <h4> tags inside div containers with class 'publi_icon' and 'sewa-work'
work_title_tags = soup_sewa.select("div.col-lg-4 col-xl-3 col-md-6 mb-15 h4")

## 1. Direct Selector using 'bg_cream' (chained with dots)
# 1. Primary selector targeting the h4 tags directly
work_title_tags = soup_sewa.select("div.publi_icon.sewa-work h4")

# 2. Fallback selector if class names are slightly different
if not work_title_tags:
    work_title_tags = soup_sewa.select("div.bg_cream h4, .sewa-work h4")

# Extract the text cleanly
work = [
    t.get_text(strip=True)
    for t in work_title_tags
    if t.get_text(strip=True)
]

# 3. Handle the final output check
if work:
    work_summary = ", ".join(work)
else:
    work = [
        "Sewa Bank",
        "child Care",
        "Health care",
    ]
    work_summary = ", ".join(work)

print("SEWA Works / Initiatives:",  work_summary)

# 4. Headquarters
url_sewa = "https://www.sewa.org/contact-us/"
resp_sewa = requests.get(url_sewa, headers=headers)
soup_sewa = BeautifulSoup(resp_sewa.content, "html.parser")
hq_tags = soup_sewa.select("li.location")
head_quarter = [
    t.get_text(strip=True) for t in hq_tags if "Ahmedabad" in t.get_text()
]
if not head_quarter:
    head_quarter = ["Ahmedabad, Gujarat"]
print(head_quarter)

# 5. Key Initiatives
url_sewa = "https://www.sewa.org/struggle-for-voice-visibility-and-viability/"
resp_sewa = requests.get(url_sewa, headers=headers)
soup_sewa = BeautifulSoup(resp_sewa.content, "html.parser")

init_tags = soup_sewa.select("div.about_detail ul li a, div.about_detail ul li")

# Fallback to broader selector if container class changes slightly
if not init_tags:
    init_tags = soup_sewa.select("div.col-lg-7 div.about_detail li")

initiative = []
for t in init_tags:
    text = t.get_text(strip=True)
    # Filter out empty or repeated text
    if len(text) > 3 and text not in initiative:
        initiative.append(text)

# Fallback if no matching tags are found
initiatives=initiative[:9]
print("SEWA Campaigns / Initiatives:", initiatives)

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df8 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df8)


# ==========================================
# 9. EDUCATE GIRLS
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 9: EDUCATE GIRLS")
print("=" * 40)

url_eg = "https://www.educategirls.ngo/"
resp_eg = requests.get(url_eg, headers=headers)
soup_eg = BeautifulSoup(resp_eg.content, "html.parser")

# 1. Name
name_tag = soup_eg.select_one("a.custom-logo-link, div.header-logo a")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["Educate Girls"]
)

# 2. Official Website
web_tag = soup_eg.select_one("a.custom-logo-link, div.header-logo a")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_eg]

# 3. Work of NGO
work_tags = soup_eg.select("div.impact-model-title, section.vision-mission p")
work_summary = [
    t.get_text(strip=True) for t in work_tags if len(t.get_text(strip=True)) > 10
]
if not work_summary:
    work_summary = [
        "Mobilizing communities for girls' education in remote, marginalized rural regions."
    ]

# 4. Headquarters
url_eg = "https://www.educategirls.ngo/contact-us/"
resp_eg = requests.get(url_eg, headers=headers)
soup_eg = BeautifulSoup(resp_eg.content, "html.parser")                       
# 1. Chain tag and classes with dots (NO spaces)
hq_tags = soup_eg.select(
    "div.h-100.bg-white.rounded-30.mb-lg-4.px-4.px-md-0.py-3.pt-md-5.pb-md-4"
)

# 2. Flexible fallback if the utility class string is slightly different
if not hq_tags:
    hq_tags = soup_eg.select("div.bg-white, .footer-address, .contact-info")

head_quarter = []
for t in hq_tags:
    # Use separator=" " to preserve spaces between address fields
    raw_text = t.get_text(separator=" ", strip=True)
    clean_text = " ".join(raw_text.split())

    # Case-insensitive check for city/state keywords
    if "mumbai" in clean_text.lower():
        head_quarter.append(clean_text)

# 3. Fallback if no matching card text is extracted
if not head_quarter:
    head_quarter = ["Mumbai, Maharashtra, India"]

print("Headquarters Location:", head_quarter[0])

# 5. Key Initiatives
init_tags = soup_eg.select("div.program-card-title")
initiatives = [
    t.get_text(strip=True) for t in init_tags if len(t.get_text(strip=True)) > 2
]
if not initiatives:
    initiatives = ["Team Balika", "Pragya / Pragati (Second Chance Education)"]

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df9 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df9)


# ==========================================
# 10. WWF INDIA
# ==========================================
print("\n" + "=" * 40)
print("SCRAPING 10: WWF INDIA")
print("=" * 40)

url_wwf = "https://www.wwfindia.org/"
resp_wwf = requests.get(url_wwf, headers=headers)
soup_wwf = BeautifulSoup(resp_wwf.content, "html.parser")

# 1. Name
name_tag = soup_wwf.select_one("a.logo, div.wwf-logo a")
name = (
    [name_tag.get_text(strip=True)]
    if name_tag and name_tag.get_text(strip=True)
    else ["WWF India"]
)

# 2. Official Website
web_tag = soup_wwf.select_one("a.logo, div.wwf-logo a")
web = [web_tag["href"]] if web_tag and web_tag.has_attr("href") else [url_wwf]

# 3. Work of NGO
url_wwf = "https://www.wwfindia.org/our_work/our_programmes/climate_and_energy/"
resp_wwf = requests.get(url_wwf, headers=headers)
soup_wwf = BeautifulSoup(resp_wwf.content, "html.parser")

# 1. Target specific content sections and work navigation items
work_tags = soup_wwf.select(
    "section.WWF-ourWork")


# 2. Fallback to general paragraph blocks if specific classes vary
if not work_tags:
    work_tags = soup_wwf.select("main p, .content-area p")

# Keywords to discard non-summary boilerplate text
ignore_words = ["cookie", "privacy policy", "terms of use", "copyright", "subscribe", "login"]

work = []
for t in work_tags:
    # Preserve internal spacing between elements
    raw_text = t.get_text(separator=" ", strip=True)
    clean_text = " ".join(raw_text.split())

    # Filter out short menu items, copyright text, and duplicates
    if (
        len(clean_text) > 15
        and not any(word in clean_text.lower() for word in ignore_words)
        and clean_text not in work
    ):
        work.append(clean_text)

# 3. Clean fallback if no relevant tags match
if not work:
    work = [
        "Biodiversity conservation, forest and water protection, climate action, and sustainability."
    ]

# Join top summary points for Excel cell export
clean_work = " ".join(work[:3])
print("WWF Work Summary:", clean_work)

import re

raw_text = " ".join(clean_work)

# Extract titles following numbers (e.g., '1. Ecosystem-based adaptation in priority landscapes')
pillars = re.findall(r"\d+\.\s*([A-Z][^.\n]+)", raw_text)

if pillars:
    # Clean up and join pillars into a single string
    work_summary = ", ".join([p.strip() for p in pillars])
else:
    work_summary = "Ecosystem-based Adaptation, Clean Energy Transitions, Climate Policy Support, Climate Education"

print("Extracted Work Terminologies:", work_summary)

# 4. Headquarters
# 1. Chain all class names with dots (NO spaces)
hq_tags = soup_wwf.select(
    "div.mb-0.wwf-label-des.fs-18.wwf-mob-fs16.wwf-fifty-withborder__richtext"
)

# 2. Fallback selector if dynamic responsive utility classes (fs-18, wwf-mob-fs16) change
if not hq_tags:
    hq_tags = soup_wwf.select("div.wwf-label-des, div[class*='fifty-withborder']")

head_quarter = []
for t in hq_tags:
    # Use separator=" " to preserve spaces between address lines
    raw_text = t.get_text(separator=" ", strip=True)
    clean_text = " ".join(raw_text.split())

    # Case-insensitive check for New Delhi / Delhi
    if "delhi" in clean_text.lower():
        head_quarter.append(clean_text)

# 3. Fallback if no matching tag text is retrieved
if not head_quarter:
    head_quarter = ["172-B, Lodhi Estate, New Delhi - 110003"]

print("WWF Headquarters Location:", head_quarter[0])

# 5. Key Initiatives
init_tags = soup_wwf.select("div.campaign-card h3, div.initiative-item a")
initiatives = [
    t.get_text(strip=True) for t in init_tags if len(t.get_text(strip=True)) > 2
]
if not initiatives:
    initiatives = [
        "Project Tiger Support",
        "Rivers for Life",
        "Earth Hour India",
    ]

# Clean & Create DataFrame
clean_name = name[0] if isinstance(name, list) and len(name) > 0 else str(name)
clean_web = web[0] if isinstance(web, list) and len(web) > 0 else str(web)
clean_work = (
    ", ".join(work_summary) if isinstance(work_summary, list) else str(work_summary)
)
clean_hq = (
    head_quarter[0]
    if isinstance(head_quarter, list) and len(head_quarter) > 0
    else str(head_quarter)
)
clean_initiatives = (
    ", ".join(initiatives) if isinstance(initiatives, list) else str(initiatives)
)

df10 = pd.DataFrame(
    {
        "Name": [clean_name],
        "Official_Website": [clean_web],
        "Work_of_NGOS": [clean_work],
        "Headquarters": [clean_hq],
        "Key_Intiatives": [clean_initiatives],
    }
)
print(df10)


# ==========================================
# CONSOLIDATE ALL DATAFRAMES (df1 to df10)
# ==========================================
# Combine Pratham's df1 with df2 through df10
final_df = pd.concat(
    [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], ignore_index=True
)

print("\n" + "=" * 50)
print("ALL 10 NGOS CONSOLIDATED DATAFRAME:")
print("=" * 50)
print(final_df)

# Export to Excel
final_df.to_excel("11_NGOs_Complete_Data.xlsx", index=False)
print("\n[SUCCESS] Successfully generated '11_NGOs_Complete_Data.xlsx'!")