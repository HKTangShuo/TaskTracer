from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    input_type = 'radio'
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'
