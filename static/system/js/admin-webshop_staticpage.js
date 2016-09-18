function rewrite_name()
{
    if (document.getElementById('id_url').value == '')
    {
        document.getElementById('id_name').addEventListener('keyup', function()
        {
            document.getElementById('id_url').value = str_to_url(this.value);
        });
    }

    if (document.getElementById('id_title').value == '')
    {
        document.getElementById('id_name').addEventListener('keyup', function()
        {
            document.getElementById('id_title').value = this.value;
        });
    }

    if (document.getElementById('id_h1').value == '')
    {
        document.getElementById('id_name').addEventListener('keyup', function()
        {
            document.getElementById('id_h1').value = this.value;
        });
    }
}
document.addEventListener("DOMContentLoaded", rewrite_name);