nginx.conf:
  file.managed:
    - name: /etc/nginx/sites-available/{{ pillar['project'] }}.conf
    - template: jinja
    - source: salt://nginx/django.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: nginx

nginx:
  pkg:
    - name: nginx
    - installed
  service.running:
    - enable: True
    - watch:
      - file: /etc/nginx/sites-available/{{ pillar['project'] }}.conf
    - require:
      - file: /etc/nginx/sites-enabled/nginx.conf

/etc/nginx/sites-enabled/nginx.conf:
  file.symlink:
    - name: /etc/nginx/sites-enabled/{{ pillar['project'] }}.conf
    - target: /etc/nginx/sites-available/{{ pillar['project'] }}.conf
    - require:
      - file: /etc/nginx/sites-available/{{ pillar['project'] }}.conf
