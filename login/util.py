# from sysmanage.models import Menu, User, Browse_record, Online, Role, Dictionary, Test, Generate
# from django.http import JsonResponse, StreamingHttpResponse
#
#
# # 返回dict
# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
#
#
# # 菜单增权限
# def role_create_rights(user_id, iframe_id):
#     user_list = User.objects.get(user_id=user_id)  # 登录用户信息列表
#     role_list = Role.objects.get(role_id=user_list.role_id)  # 登录用户角色列表
#     rights = 'false'
#     if role_list.role_create_rights:
#         if Menu.objects.extra(where=['id IN(' + role_list.role_create_rights + ')']).filter(
#                 id=iframe_id).count() > 0:
#             rights = 'true'
#
#     return rights
#
#
# # 菜单删权限
# def role_delete_rights(user_id, iframe_id):
#     user_list = User.objects.get(user_id=user_id)  # 登录用户信息列表
#     role_list = Role.objects.get(role_id=user_list.role_id)  # 登录用户角色列表
#     rights = 'false'
#     if role_list.role_delete_rights:
#         if Menu.objects.extra(where=['id IN(' + role_list.role_delete_rights + ')']).filter(
#                 id=iframe_id).count() > 0:
#             rights = 'true'
#
#     return rights
#
#
# # 菜单改权限
# def role_update_rights(user_id, iframe_id):
#     user_list = User.objects.get(user_id=user_id)  # 登录用户信息列表
#     role_list = Role.objects.get(role_id=user_list.role_id)  # 登录用户角色列表
#     rights = 'false'
#     if role_list.role_update_rights:
#         if Menu.objects.extra(where=['id IN(' + role_list.role_update_rights + ')']).filter(
#                 id=iframe_id).count() > 0:
#             rights = 'true'
#
#     return rights
#
#
# # 菜单查权限
# def role_select_rights(user_id, iframe_id):
#     user_list = User.objects.get(user_id=user_id)  # 登录用户信息列表
#     role_list = Role.objects.get(role_id=user_list.role_id)  # 登录用户角色列表
#     rights = 'false'
#     if role_list.role_select_rights:
#         if Menu.objects.extra(where=['id IN(' + role_list.role_select_rights + ')']).filter(
#                 id=iframe_id).count() > 0:
#             rights = 'true'
#
#     return rights
