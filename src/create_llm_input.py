import click
from jinja2 import Template


@click.command()
@click.option('--tsv', prompt='Enter tab-separated values (title, altTitle, source, custodian, topics, keywords, abstract, lineage)')
def generate_json(tsv):
    # Split the input by tab
    items = tsv.split('\t')
    
    # Ensure we have exactly 8 items, fill missing with empty strings
    while len(items) < 8:
        items.append('')
    
    # Define the template
    template_str = '''
    {
        "title": "{{ title | default('') | escape }}",
        "altTitle": "{{ altTitle | default('') | escape }}",
        "source": "{{ source | default('') | escape }}",
        "custodian": "{{ custodian | default('') | escape }}",
        "topics": "{{ topics | default('') | escape }}",
        "keywords": "{{ keywords | default('') | escape }}",
        "abstract": "{{ abstract | default('') | escape }}",
        "lineage": "{{ lineage | default('') | escape }}"
    }
    '''
    
    # Create a template object
    template = Template(template_str)
    
    # Render the template with the provided values
    rendered_json = template.render(
        title=items[0],
        altTitle=items[1],
        source=items[2],
        custodian=items[3],
        topics=items[4],
        keywords=items[5],
        abstract=items[6],
        lineage=items[7]
    )
    
    # Print the rendered JSON
    print(rendered_json)

if __name__ == '__main__':
    generate_json()