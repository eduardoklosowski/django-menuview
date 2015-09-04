__version__ = '0.1.dev0'
__license__ = 'MIT'


from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.utils import six
from functools import total_ordering


try:
    HIDE_EMPTY_MENU = getattr(settings, 'MENUVIEW_HIDE_EMPTY_MENU', False)
except ImproperlyConfigured:
    HIDE_EMPTY_MENU = False


@total_ordering
class BaseMenu(object):
    def __init__(self, title, url, order=0, html_title=None, permission_required=None, parent=None):
        self.parent = parent
        self.title = title
        self.html_title = html_title
        self.url = url
        if permission_required and isinstance(permission_required, six.string_types):
            permission_required = (permission_required,)
        self.permission_required = permission_required
        self.order = order

    def __eq__(self, other):
        return self.__cmp() == other.__cmp()

    def __lt__(self, other):
        return self.__cmp() < other.__cmp()

    def __cmp(self):
        return (self.order, self.title)

    def get_html_title(self):
        if self.html_title is not None:
            return self.html_title
        return self.title


class MenuItem(BaseMenu):
    def html(self, user):
        if user and self.permission_required and not user.has_perms(self.permission_required):
            return ''
        return '<li><a href="%s">%s</a></li>' % (self.url, self.get_html_title())


class Menu(BaseMenu):
    def __init__(self, title, url=None, order=0, html_title=None, permission_required=None, parent=None):
        super(Menu, self).__init__(title, url, order=order, html_title=html_title,
                                   permission_required=permission_required, parent=parent)
        self.children = []

    def __add_item_order(self, item):
        for i in range(len(self.children)):
            if item < self.children[i]:
                self.children.insert(i, item)
                return
        self.children.append(item)

    def add_item(self, title, url, order=0, html_title=None, permission_required=None):
        item = MenuItem(title, url, order=order, html_title=html_title,
                        permission_required=permission_required, parent=self)
        self.__add_item_order(item)

    def create_submenu(self, title, url, order=0, html_title=None, permission_required=None):
        menu = Menu(title, url, order=order, html_title=html_title,
                    permission_required=permission_required, parent=self)
        self.__add_item_order(menu)
        return menu

    def filter_children_permission(self, user):
        return [item for item in self.children
                if not item.permission_required or user.has_perms(item.permission_required)]

    def html(self, user=None):
        items = self.children_html(user)
        if HIDE_EMPTY_MENU and not items:
            return ''
        title = self.get_html_title()
        if self.url:
            title = '<a href="%s">%s</a>' % (self.url, title)
        return '<li>%s<ul>%s</ul></li>' % (title, items)

    def children_html(self, user=None):
        if user:
            items = self.filter_children_permission(user)
        else:
            items = self.children
        return ''.join(item.html(user) for item in items)

    def add(self, title, order=0, html_title=None, permission_required=None):
        def func(view):
            if permission_required is None and hasattr(view, 'permission_required'):
                perm = view.permission_required
            else:
                perm = permission_required
            self.add_item(title, reverse_lazy(view.urlname), order=order,
                          html_title=html_title, permission_required=perm)
            return view
        return func
