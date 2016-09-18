include:
  - requirements
  - postgresql

/usr/lib/libjpeg.so:
  file.symlink:
    - target: /usr/lib/x86_64-linux-gnu/libjpeg.so

/usr/lib/libfreetype.so:
  file.symlink:
    - target: /usr/lib/x86_64-linux-gnu/libfreetype.so

/usr/lib/libz.so:
  file.symlink:
    - target: /usr/lib/x86_64-linux-gnu/libz.so

project_dir:
  file.symlink:
    - name: /home/vagrant/{{ pillar['project'] }}/{{ pillar['project']|replace('.', '_') }}
    - target: /vagrant
    - makedirs: True
    - user: vagrant
    - group: vagrant

venv:
  virtualenv.managed:
    - name: /home/vagrant/{{ pillar['project'] }}/env
    - no_site_packeges: True
    - runas: vagrant
    - user: vagrant
    - group: vagrant
    - python: /usr/bin/python3.4
    - requirements: salt://django/requirements.txt
    - require:
      - pkg: python3.4-dev
      - pkg: python-virtualenv
      - pkg: libpq-dev
      - pkg: libevent-dev
      - pkg: libjpeg-dev
      - pkg: libfreetype6-dev
      - pkg: zlib1g-dev
      - pkg: gcc
      - file: /usr/lib/libz.so
      - file: /usr/lib/libfreetype.so
      - file: /usr/lib/libjpeg.so

djangouser:
  postgres_user.present:
    - name: {{ pillar['dbuser'] }}
    - password: {{ pillar['dbpassword'] }}
    - runas: postgres
    - require:
      - service: postgresql

djangodb:
  postgres_database.present:
    - name: {{ pillar['dbname'] }}
    - encoding: UTF8
    - lc_ctype: en_US.UTF8
    - lc_collate: en_US.UTF8
    - template: template0
    - owner: {{ pillar['dbuser'] }}
    - runas: postgres
    - require:
      - postgres_user: djangouser

create Django project:
  cmd.run:
    - user: vagrant
    - name: ". env/bin/activate && python {{ pillar['project']|replace('.', '_') }}/manage.py migrate && cd {{ pillar['project']|replace('.', '_') }} && python manage.py collectstatic --noinput && python manage.py loaddata --ignorenonexistent start_fixture.json"
    - cwd: /home/vagrant/{{ pillar['project'] }}/
    - require:
      - virtualenv: venv
      - pkg: python3.4-dev
      - file: pg_hba.conf
      - file: project_dir
