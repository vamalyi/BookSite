(function(){

    var transliteration_default_config = {
        'а': 'a',   'б': 'b',   'в': 'v',
        'г': 'g',   'д': 'd',   'е': 'e',
        'ё': 'e',   'ж': 'zh',  'з': 'z',
        'и': 'i',   'й': 'y',   'к': 'k',
        'л': 'l',   'м': 'm',   'н': 'n',
        'о': 'o',   'п': 'p',   'р': 'r',
        'с': 's',   'т': 't',   'у': 'u',
        'ф': 'f',   'х': 'h',   'ц': 'c',
        'ч': 'ch',  'ш': 'sh',  'щ': 'sch',
        'ь': '',  'ы': 'y',   'ъ': '',
        'э': 'e',   'ю': 'yu',  'я': 'ya',

        'А': 'a',   'Б': 'b',   'В': 'v',
        'Г': 'g',   'Д': 'd',   'Е': 'e',
        'Ё': 'e',   'Ж': 'zh',  'З': 'z',
        'И': 'i',   'Й': 'y',   'К': 'k',
        'Л': 'l',   'М': 'm',   'Н': 'n',
        'О': 'o',   'П': 'p',   'Р': 'r',
        'С': 's',   'Т': 't',   'У': 'u',
        'Ф': 'f',   'Х': 'h',   'Ц': 'c',
        'Ч': 'ch',  'Ш': 'sh',  'Щ': 'sch',
        'Ь': '',  'Ы': 'y',   'Ъ': '',
        'є': 'e', 'Є': 'e', 'ї': 'i', 'Ї': 'i',
        'Э': 'e',   'Ю': 'yu',  'Я': 'ya'
    };

    var transliteration_url_config = {
        ' ': '-',     '\\': '',    '`':'',
        '?': '',    '-': '-',      '.': '',
        '*':'',       '{':'',        ',':'',
        '&':'',       '}':'',        '\'':'',
        '^':'',       ']':'',        ';':'',
        '%':'',       '=':'',        ':':'',
        '$':'',       '+':'',        '"':'',
        '#':'',       '_':'_',        '|':'',
        '№':'',       ')':'',        '/':'',
        '@':'',       '(':'',        '[':'',
        '!':'',      '~':''
    };

    function chr_to_translit(c)
    {
        if(transliteration_default_config[c] !== undefined)
        {
            return transliteration_default_config[c];
        }
        return c;
    }

    function chr_to_url(c)
    {
        c = chr_to_translit(c);
        if(transliteration_url_config[c] !== undefined)
        {
            return transliteration_url_config[c];
        }
        return c;
    }

    function str_to_translit(s)
    {
        var t = '';
        for(var i=0; i< s.length; i++)
        {
            t += chr_to_translit(s[i]);
        }
        return t;
    }

    function str_to_url(s)
    {
        var t = '';
        for(var i=0; i< s.length; i++)
        {
            t += chr_to_url(s[i]);
        }
        return t;
    }

    window.str_to_translit = str_to_translit;
    window.str_to_url = str_to_url;

}());