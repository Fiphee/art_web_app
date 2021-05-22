from django import template

register = template.Library()


@register.filter
def middle_pages(page_obj, current_page):
    pages = []

    if current_page.has_previous():
        previous_page = current_page.previous_page_number() 
        if previous_page != 1:
            pages.append(previous_page)

    if current_page.number not in [1, page_obj.num_pages]:
        pages.append(current_page.number)
        
    if current_page.has_next():
        next_page = current_page.next_page_number()
        if next_page != page_obj.num_pages:
            pages.append(next_page)

    return pages


@register.filter
def far_from_edge(page, page_obj=None):
    if page_obj:
        if page_obj.num_pages - page > 1:
            return True
        return False

    if page - 1 > 1:
        return True
    return False