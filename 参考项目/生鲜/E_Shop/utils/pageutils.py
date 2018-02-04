#! /usr/bin env python3
# -*- coding:utf-8 -*-


# 分页工具类
class MultiObjectReturned():
    per_page = 12
    objects = None
    objects_name = 'objects'

    def get_objects(self, page_num='1'):
        from django.core.paginator import Paginator
        page_num = int(page_num)
        paginator = Paginator(self.objects, self.per_page)

        # 有效性处理
        if page_num < 1:
            page_num = 1
        if page_num > paginator.num_pages:
            page_num = paginator.num_pages

        page = paginator.page(page_num)

        # paginator.page_range是xrange，可迭代
        return {
            'page': page,
            'page_range': paginator.page_range,
            self.objects_name: page.object_list
        }
