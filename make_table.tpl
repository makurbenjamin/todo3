%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  <td><a href="/edit/{{row[0]}}">Edit</a></td>
</tr> 
%end
</table>

<p>Create a new task <a href="/new">here</a></p>
