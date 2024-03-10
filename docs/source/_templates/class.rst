{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. add toctree option to make autodoc generate the pages

.. autoclass:: {{ objname }}
   :members:
   
{% block attributes %}
{% if attributes %}
.. rubric:: Attributes

.. autosummary::
{% for item in attributes %}
   ~{{ fullname }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block methods %}
{% if methods %}
.. rubric:: Methods

.. autosummary::
{% for item in methods %}
   {%- if item != '__init__' %}
   ~{{ fullname }}.{{ item }}
   {%- endif -%}
{%- endfor %}
{% endif %}
{% endblock %}