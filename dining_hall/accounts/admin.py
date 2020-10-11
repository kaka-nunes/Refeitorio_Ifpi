from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dining_hall.accounts.models import User, Servant, Student


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'username', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_admin', 'is_superuser']
    search_fields = ['name', 'phone', 'email']
    ordering = ['created_at',]
    filter_horizontal = ['user_permissions']

    fieldsets = [
        ['Informações pessoais', {'fields': ['name', 'username', 'email']}],
        [
            'Permissões',
            {'fields': [
                'is_active', 'is_staff', 'is_admin', 'is_superuser',
                'user_permissions'
                ]
            }
        ],
    ]

    add_fieldsets = [
        [
            'Informações Pessoais',
            {'fields': [
                'name', 'username', 'email', 'password', 'password2'
                ]
            }
        ],
        [
            'Permissões',
            {'fields': [
                'is_active', 'is_staff', 'is_admin', 'is_superuser',
                'user_permissions'
                ]
            }
        ],
    ]


class ServantAdmin(UserAdmin):
    list_display = [
        'name', 'username', 'entry_date', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = [
        'name', 'username', 'entry_date', 'is_active', 'is_staff', 'created_at'
    ]
    search_fields = ['name', 'email', 'username']
    ordering = ['created_at', 'name', 'entry_date']

    fieldsets = [
        [
            'Informações Pessoais', {'fields': [
                'name', 'username', 'email', 'entry_date',
                ]
            }
        ],
        [
            'Permissões',
            {'fields': ['is_active', 'is_staff', 'is_admin', 'is_superuser']
            }
        ],
    ]

    add_fieldsets = [
        ['Personal info', {
            'fields': [
                'name', 'username', 'email', 'entry_date',
                'password1', 'password2'
                ]
            }
        ],
        [
            'Permissions',
            {'fields': ['is_active', 'is_staff', 'is_admin', 'is_superuser']
            }
        ],
    ]


class StudentAdmin(UserAdmin):
    list_display = [
        'name', 'username', 'student_class', 'entry_date', 'birthdate',
        'cpf', 'rg', 'is_active', 'is_staff', 'created_at', 
    ]
    list_filter = [
        'name', 'username', 'birthdate', 'is_active', 'cpf', 'rg',
        'is_staff', 'created_at'
    ]
    search_fields = [
        'name', 'email', 'username', 'student_class', 'entry_date'
    ]
    ordering = [
        'created_at', 'name', 'birthdate', 'student_class', 'entry_date',
        'username'
        ]

    fieldsets = [
        [
            'Personal info', {'fields': [
                'name', 'username', 'email', 'phone', 'birthdate', 'cpf',
                'rg', 'profilepic', 'student_class', 'entry_date',
                ]
            }
        ],
        [
            'Permissions',
            {'fields': ['is_active', 'is_staff', 'is_admin', 'is_superuser']
            }
        ],
    ]

    add_fieldsets = [
        ['Personal info', {
            'fields': [
                'name', 'username', 'email', 'phone', 'cpf', 'rg',
                'birthdate', 'profilepic', 'student_class', 'entry_date',
                'password1', 'password2'
                ]
            }
        ],
        [
            'Permissions',
            {'fields': ['is_active', 'is_staff', 'is_admin', 'is_superuser']
            }
        ],
    ]


# Admin registration for models
admin.site.register(Servant, ServantAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, CustomUserAdmin)