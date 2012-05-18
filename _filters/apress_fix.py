import re

def fixup_codeblock(match):
    text = match.group(1).strip()
    text = text.replace('<br />', '')
    lang = ('html' if text.startswith(('<', '&lt;'))
            else 'bash' if text.startswith('$')
            else 'python')
    return '<pre>\n#!{}\n{}</pre>'.format(lang, text)

def run(content):
    content = re.sub(r'<a id="page_\d+" />', '', content)
    content = re.sub(
        r'(?s)<div class="pl">\n<code>(.*?)</code>\n</div>',
        fixup_codeblock,
        content
        )
    return content
