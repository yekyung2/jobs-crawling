import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=pm&l=%EC%84%9C%EC%9A%B8&jt=new_grad&limit={LIMIT}&radius=25"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    last_page = pages[-1]
    return last_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"}).get_text("\n", strip=True)
    location = html.find("span", {"class": "location"}).string
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=pm&l=%EC%84%9C%EC%9A%B8&jt=new_grad&limit=50&radius=25&start=150&vjk={job_id}",
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed : page : {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
        return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
