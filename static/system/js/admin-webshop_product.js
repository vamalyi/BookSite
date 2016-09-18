function rewrite_name()
{
    // if (document.getElementById('id_code').value == '')
    // { document.getElementById('id_name').addEventListener('keyup', function()
    //     {
    //         document.getElementById('id_code').value = str_to_translit(this.value);
    //     });
    // }

    if (document.getElementById('id_url').value == '')
    {
        document.getElementById('id_name').addEventListener('keyup', function()
        {
            document.getElementById('id_url').value = str_to_url(this.value);
        });
    }
}
document.addEventListener("DOMContentLoaded", rewrite_name);