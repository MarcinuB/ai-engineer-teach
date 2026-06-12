import time
import anthropic

def create_with_retry(client: anthropic.Anthropic, max_retries: int = 3, **kwargs):
    """Drop-in wrapper around client.messages.create with retry logic"""
    
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            print (f"[retry] {type(e).__name__}, waiting {wait}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
            
        except anthropic.APIStatusError as e:
            if e.status_code < 500:
                raise
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            print(f"[retry] {e.status_code} server error, waiting {wait}s")
            time.sleep(wait)