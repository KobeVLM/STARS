from django import template
from django.utils.safestring import mark_safe
import markdown
import bleach

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """
    Renders markdown safely.
    Only allows basic formatting (bold, italic) to prevent abuse and script injection.
    """
    if not text:
        return ""
        
    # Render markdown to HTML
    html = markdown.markdown(text)
    
    # Allowed tags and attributes for bleach
    allowed_tags = ['p', 'strong', 'em', 'b', 'i']
    
    # Clean the HTML
    cleaned_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes={},
        strip=True
    )
    
    return mark_safe(cleaned_html)
