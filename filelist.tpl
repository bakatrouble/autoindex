<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Directory Index: /{{ path }}</title>
    <link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon" />
    <link href="/~static/darkly.css" rel="stylesheet" type="text/css" />
    <link href="/~static/icons.css" rel="stylesheet" type="text/css" />
    <style>
        table tbody tr td {
            padding: 0 !important;
        }
        table tbody tr td a,
        table tbody tr td span {
            display: block;
            padding: .3rem;
        }
    </style>
</head>
<body>
    <div class="container" style="padding: 15px 0">
        <h1 class="h3">Directory Index: /{{ path }}</h1>
        <table class="table table-hover table-bordered table-sm">
            <thead>
                <tr>
                    <th><a href="{{ get_sort_link(sort, 'name', hidden) }}">
                        Name {{ get_sort_icon('name', sort) | safe }}
                    </a></th>
                    <th style="width: 100px;"><a href="{{ get_sort_link(sort, 'size', hidden) }}">
                        Size {{ get_sort_icon('size', sort) | safe }}
                    </a></th>
                    <th style="width: 170px;"><a href="{{ get_sort_link(sort, 'created', hidden) }}">
                        Created {{ get_sort_icon('created', sort) | safe }}
                    </a></th>
                </tr>
            </thead>
            <tbody>
                {% for item in lst %}
                    {% with dir=item.is_dir, file=not item.is_dir %}
                    <tr>
                        <td>
                            <a href="{{ item.link_name }}{% if dir %}{{ query }}{% endif %}" {% if file %}download{% endif %}>
                                {{ item.icon | safe }} {{ item.display_name }}
                            </a>
                        </td>
                        <td>{% if file %}<span title="{{ item.size }} bytes">{{ item.formatted_size }}</span>{% endif %}</td>
                        <td><span>{{ item.formatted_date }}</span></td>
                    </tr>
                    {% endwith %}
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
