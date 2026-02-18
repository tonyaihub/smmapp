from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_article(keyword, word_count=1500):
    competitors = analyze_competitors(keyword)
    prompt = f"Write a SEO-optimized article on '{keyword}' ( {word_count} words). Analyze competitors: {', '.join(competitors)}. Include H1-H3 headings, meta description, internal/external links, natural tone. Optimize for {config.NICHE} audience: {config.TARGET_AUDIENCE}."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    meta_desc = content.split('\n')[0][:160]  # Extract meta
    return content, meta_desc