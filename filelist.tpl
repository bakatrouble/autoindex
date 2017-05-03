<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File list</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.10/components/reset.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.10/components/site.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.10/components/icon.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.10/components/table.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.10/components/container.min.css" rel="stylesheet" />
    <style>
        table tbody tr a {
            display: block;
        }
    </style>
</head>
<body>
    <div class="ui main container" style="padding: 15px 0">
        <h2>Directory Index - /{{ path }}</h2>
        <table class="ui selectable unstackable table">
            <thead>
                <tr>
                    <th><a href="{{ get_sort_link(sort, 'name', hidden) }}">
                        Name {{ !get_sort_icon('name', sort) }}
                    </a></th>
                    <th style="width: 100px;"><a href="{{ get_sort_link(sort, 'size', hidden) }}">
                        Size {{ !get_sort_icon('size', sort) }}
                    </a></th>
                    <th style="width: 170px;"><a href="{{ get_sort_link(sort, 'created', hidden) }}">
                        Created {{ !get_sort_icon('created', sort) }}
                    </a></th>
                </tr>
            </thead>
            <tbody>
                % if path:
                    <tr>
                        <td class="selectable">
                            <a href="../{{ f'?{query}' if query else '' }}">
                                <i class="level up icon"></i>
                                ../
                            </a>
                        </td>
                        <td></td>
                        <td></td>
                    </tr>
                % end
                % for item in lst:
                    <tr>
                    % if item.isdir:
                            <td class="selectable">
                                <a href="{{ item.name }}/{{ f'?{query}' if query else '' }}">
                                    <i class="folder outline icon"></i>
                                    {{ item.name }}/
                                </a>
                            </td>
                            <td></td>
                            <td></td>
                    % else:
                            <td class="selectable">
                                <a href="/_/{{ path }}{{ item.name }}" target="_blank">
                                    <i class="file {{ get_file_icon(item.name) }} outline icon"></i>
                                    {{ item.name }} [{{ guess_type(item.name)[0] }}]
                                </a>
                            </td>
                            <td><span title="{{ item.size }} byte(s)">{{ format_size(item.size) }}</span></td>
                            <td>{{ format_date(item.created) }}</td>
                    % end
                    </tr>
                % end
            </tbody>
        </table>
    </div>
</body>
</html>
