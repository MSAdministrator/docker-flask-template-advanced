function poll() {
    $.ajax("{{url_for('processor_bp.get_processor_status', id=job_id)}}", {
        dataType: "json"
        , success: function(resp) {
            if(resp.progress >= 0.99 && resp.result) {
                var result = resp.result;
                var table = '';
                for(var key in result){
                    console.log(key)
                    console.log(result[key])
                    table += '<tr>';
                    table += '<td>' + key + '</td>';
                    table += '<td>' + result[key] + '</td>';
                    table += '</tr>';
                }
                var tbody = document.getElementById('search').innerHTML = table
                document.getElementById("search-status").style.display = "none";
                document.getElementById("results").style.display = "block";
                return;
            } else {
                document.getElementById("search-status").style.display = "block";
                setTimeout(poll, 500.0);
            }
        }
    });
}

function exists(domain) {
    $.ajax("{{url_for('search_bp.data_exists', domain=DOMAIN)}}", {
        dataType: "json"
        , success: function(result) {
            var table = '';
            for(var key in result){
                console.log(key)
                console.log(result[key])
                table += '<tr>';
                table += '<td>' + key + '</td>';
                table += '<td>' + result[key] + '</td>';
                table += '</tr>';
            }
            var tbody = document.getElementById('search').innerHTML = table
            document.getElementById("search-status").style.display = "none";
            document.getElementById("results").style.display = "block";
            return;
        }
    });
}