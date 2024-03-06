from typing import Dict, Any, List

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context

from tree_menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/tree_menu.html', takes_context=True)
def draw_menu(context: Context, menu: str) -> Dict[str, Any]:
    """
    Шаблонный тег для отображения древовидного меню.
    """

    try:
        # Получает все пункты меню
        items = MenuItem.objects.filter(menu__title=menu)
        items_values = items.values()

        # Получает элементы корневого меню (без родителя)
        root_item = [item for item in items_values.filter(parent=None)]

        # Определяет идентификатор выбранного пункта меню из параметров запроса
        selected_item_id = int(context['request'].GET[menu])
        selected_item = items.get(id=selected_item_id)

        # Получает список идентификаторов выбранных пунктов меню
        selected_item_id_list = get_selected_item_id_list(selected_item, root_item, selected_item_id)

        # Добавляет дочерние элементы для каждого выбранного пункта меню.
        for item in root_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)

        result_dict = {'items': root_item}

    except (KeyError, ObjectDoesNotExist):
        # В случае ошибки возвращает список пунктов меню без родительских элементов.
        result_dict = {
            'items': [
                item for item in MenuItem.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    # Добавляет имя меню и дополнительную строку запроса в словарь result_dict.
    result_dict['menu'] = menu
    result_dict['other_querystring'] = build_querystring(context, menu)

    return result_dict


def build_querystring(context: Context, menu: str) -> str:
    """
    Создает строку запроса на основе текущего контекста.
    """

    # Инициализирует список для хранения аргументов строки запроса
    querystring_args = []

    # Перебирает все параметры текущего запроса.
    for key in context['request'].GET:
        # Если ключ текущего параметра не соответствует переданному параметру меню
        if key != menu:
            # Добавляет пару «ключ=значение» в список аргументов строки запроса.
            querystring_args.append(f"{key}={context['request'].GET[key]}")

    # Объединяет аргументы из списка в одну строку запроса, разделенную символом «&».
    querystring = '&'.join(querystring_args)

    # Возвращает готовые строки запроса
    return querystring


def get_child_items(items_values, current_item_id, selected_item_id_list):
    """
    Возвращает список дочерних элементов для данного идентификатора элемента меню.
    """
    item_list = [item for item in items_values.filter(parent_id=current_item_id)]
    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)
    return item_list


def get_selected_item_id_list(parent: MenuItem, primary_item: List[MenuItem], selected_item_id: int) -> List[int]:
    """
    Возвращает список идентификаторов выбранных пунктов меню, начиная с родительского элемента и заканчивая текущим.
    """
    selected_item_id_list = []

    while parent:
        selected_item_id_list.append(parent.id)
        parent = parent.parent
    if not selected_item_id_list:
        for item in primary_item:
            if item.id == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
