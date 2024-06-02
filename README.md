Application made in python and custom tkinter
Server written in FastApi

Current minor features:
  - If answer is correct, sends time spent on the question, player's name, player's pc no. and the question no. to the server.
  - Time spent on each question is tracked.
  - Text typed on each question is tracked and is replaced when the user changes questions.

Issues with the software:
  - Requests are not implemented the 'ideal' way.
  - I'm sure there are a lot of bugs just waiting to be found out.
  - Font sizes are not ideal, work can be done on styling
  - Uses json for storing questions and model answers

What improvements can be done:
  - Implement syntax highlighting, autocomplete, etc.
  - Add difficulty level to questions.
  - Host the server to cloud instead of local network.
  - Add leaderboards.
  - Improve user experience, design, etc.
