from fastapi import FastAPI, Request
from fastapi.responses import HTML_Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown
import os

app = FastAPI()

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content" / "blog"
TEMPLATES_DIR = BASE_DIR / "src" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTML_Response)
async def read_root(request: Request):
    # List blog posts
    posts = []
    if CONTENT_DIR.exists():
        for file in CONTENT_DIR.glob("*.mdx"):
            posts.append({
                "slug": file.stem,
                "title": file.stem.replace("-", " ").title()
            })
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "posts": posts,
        "status": "Operational",
        "brand_color": "#06B6D4"
    })

@app.get("/blog/{slug}", response_class=HTML_Response)
async def read_post(request: Request, slug: str):
    file_path = CONTENT_DIR / f"{slug}.mdx"
    if not file_path.exists():
        return HTML_Response(content="Post not found", status_code=404)
    
    content = file_path.read_text()
    # Basic MDX handling (strip frontmatter for display)
    if "---" in content:
        content = content.split("---", 2)[-1]
        
    html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
    
    return templates.TemplateResponse("post.html", {
        "request": request,
        "title": slug.replace("-", " ").title(),
        "content": html_content
    })
