"""

Note: This code uses Streamlit to create a user-friendly interface for the Sudoku Solver.

"""
import streamlit as st
import pandas as pd
from Sudoku_Solver import solve_from_line

st.title("Sudoku Solver")
st.markdown("Enter your Sudoku board below")

# Sample preset puzzles
preset_puzzles = {
    "Easy": "000000000000003085001020000000507000004000100090000000500000073002010000000040009",
    "Medium": "100070009008096300050000020010000000940060072000000040030000080004720100200050003",
    "Escargot": "100007090030020008009600500005300900010080002600004000300000010041000007007000300",
    "Steering Wheel": "000102000060000070008000900400000003050007000200080001009000805070000060000304000",
    "Arto Inkala": "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
}

option = st.selectbox("Select a sample puzzle", list(preset_puzzles.keys()))
preset_line = preset_puzzles[option]

st.markdown("### Enter Sudoku:")
with st.form("sudoku_form"):
    board = []
    # Create a 9x9 input grid
    for row in range(9):
        cols = st.columns(9)
        row_values = []
        for col in range(9):
            cell_index = row * 9 + col
            default_val = int(preset_line[cell_index])
            cell_val = cols[col].number_input(
                label="",
                min_value=0,
                max_value=9,
                value=default_val,
                key=f"cell_{row}_{col}"
            )
            row_values.append(cell_val)
        board.append(row_values)
    submitted = st.form_submit_button("Solve Puzzle")

def build_html_table(board):
    """Function to create an HTML table with thick borders to separate 3x3 blocks."""
    html = '<table style="border-collapse: collapse; margin: auto;">'
    for i in range(9):
        html += '<tr>'
        for j in range(9):
            cell_value = board[i][j]
            style = "width: 40px; height: 40px; text-align: center; font-size: 20px;"
            # Set borders: thick top/left edges and thicker borders at the end of each 3x3 block
            border_top = "2px solid black" if i == 0 else "1px solid gray"
            border_left = "2px solid black" if j == 0 else "1px solid gray"
            border_right = "2px solid black" if (j + 1) % 3 == 0 else "1px solid gray"
            border_bottom = "2px solid black" if (i + 1) % 3 == 0 else "1px solid gray"
            style += f"border-top: {border_top}; border-left: {border_left}; border-right: {border_right}; border-bottom: {border_bottom};"
            html += f'<td style="{style}">{cell_value}</td>'
        html += '</tr>'
    html += '</table>'
    return html

if submitted:
    # Convert the input board to an 81-digit string (0 represents empty cells)
    puzzle_line = "".join(str(cell) for row in board for cell in row)
    with st.spinner("Solving..."):
        solution_line = solve_from_line(puzzle_line, verbose=False)
    # Convert the solution string back to a 9x9 board
    solution_board = [[int(solution_line[i * 9 + j]) for j in range(9)] for i in range(9)]
    st.success("Puzzle solved!")
    st.markdown("### Result:")
    # Display the result table with clear 3x3 block separations
    st.markdown(build_html_table(solution_board), unsafe_allow_html=True)
