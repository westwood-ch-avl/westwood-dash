import { format, sub } from 'date-fns';
import Papa from 'papaparse';

export function objs_to_csv_string(arr){

    var column_names = [];

    d = new Date();
    
    for (var i = 1; i < 20; i++){

        var date_to_check = sub(d, {months: i});

        month_day_string = format(date_to_check, 'YYYY-MM');

        if (month_day_string in arr[0]){
            column_names.push(month_day_string);
        }

    }

    column_names.sort()

    column_names.unshift('user_id');

    //do the next step, build the csv string ... TODO

    csv_string = column_names.join(',') + '\n';

    for (var i = 0; i < arr.length; i++){

        line = ""

        for (var j = 0; j < column_names.length; j++){

            line += arr[i][column_names[j]] + ',';

        }

        csv_string += line.slice(0, -1) + '\n';

    }

    return csv_string.trim();

}

export function csv_string_to_arrays(csv_string){
    
    var results = Papa.parse(csv_string, {header: false});
    return results.data;
}

export function csv_arrays_to_table(arr){
    var table = $("<table class='table table-striped table-bordered table-hover'></table>");
    var header = $("<tr></tr>");
    
    for (var j = 0; j < arr[0].length; j++){
        header.append("<th>" + arr[0][j] + "</th>");
    }

    table.append(header);

    for (var i = 1; i < arr.length; i++){
        var row = $("<tr></tr>");
        for (var j = 0; j < arr[i].length; j++){
            row.append("<td>" + arr[i][j] + "</td>");
        }
        table.append(row);
    }

    return table[0];
}