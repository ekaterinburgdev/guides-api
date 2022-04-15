from app.models import PageElement


def serialize_page_element(pageElement):
    items = pageElement.content["items"]
    items = map(lambda x: PageElement.objects.get(id=x), items)
    items = list(map(serialize_column_list, items))
    return items


def serialize_column_list(pageElement):
    columnListId = pageElement.id
    columns = pageElement.content["items"]
    columns = map(lambda x: PageElement.objects.filter(id=x), columns)
    columns = filter(lambda x: len(x) > 0, columns)
    columns = map(lambda x: x.first(), columns)
    columns = list(map(serialize_column, columns))
    return {"columnListId": columnListId, "columns": columns}


def serialize_column(pageElement):
    columnId = pageElement.id
    columnsItems = pageElement.content["items"]
    columnsItems = map(lambda x: PageElement.objects.get(id=x), columnsItems)
    columnsItems = list(map(serialize_item, columnsItems))
    return {"columnId": columnId, "columnsItems": columnsItems}


def serialize_item(pageElement):
    itemId = pageElement.id
    itemType = pageElement.type.lower()
    return {"itemId": itemId, "type": itemType, itemType: pageElement.content}
