const nBoard = (n) =>
    Array(n)
        .fill()
        .map(() => Array(n).fill(0));

const getColumn = (arr, col) => arr.map((row) => row[col]);

const clone = (arr) => JSON.parse(JSON.stringify(arr));

const printBoard = (arr) => {
    let board = "";

    for (let row = 0; row < arr.length; row++) {
        for (let col = 0; col < arr.length; col++) {
            if (arr[row][col] == 2) 
                board += "Q"
            else 
                board += "."
        }
        board += "\n"
    }
    console.log(board);
}

function isSafe(board, qRow, qCol) {
    const n = board.length;

    //r
    for (let i = 0; i < n; i++) {
        if (newBoard[i][qCol] == 1) return false
    }

    //column
    for (let i = 0; i < n; i++) {
        newBoard[qRow][i] = 1;
    }

    //upper left diagonal
    for (let i = qRow, j = qCol; i >= 0 && j >= 0; i--, j--) {
        newBoard[i][j] = 1;
    }

    //lower left diagonal
    for (let i = qRow, j = qCol; i >= 0 && j < n; i--, j++) {
        newBoard[i][j] = 1;
    }

    //upper right diagonal
    for (let i = qRow, j = qCol; i < n && j < n; i++, j++) {
        newBoard[i][j] = 1;
    }

    //lower right diagonal
    for (let i = qRow, j = qCol; i < n && j >= 0; i++, j--) {
        newBoard[i][j] = 1;
    }

}

function placeQueen(board, qRow, qCol) {
    const n = board.length;
    const newBoard = clone(board);
    // printBoard(board)

    //r
    for (let i = 0; i < n; i++) {
        if (newBoard[i][qCol] !== 2)
            newBoard[i][qCol] = 1;
    }

    //column
    for (let i = 0; i < n; i++) {
        if (newBoard[i][qRow] !== 2)
            newBoard[qRow][i] = 1;
    }

    //upper left diagonal
    for (let i = qRow, j = qCol; i >= 0 && j >= 0; i--, j--) {
        if (newBoard[i][j] !== 2)
            newBoard[i][j] = 1;
    }

    //lower left diagonal
    for (let i = qRow, j = qCol; i >= 0 && j < n; i--, j++) {
        if (newBoard[i][j] !== 2)
            newBoard[i][j] = 1;
    }

    //upper right diagonal
    for (let i = qRow, j = qCol; i < n && j < n; i++, j++) {
        if (newBoard[i][j] !== 2)
            newBoard[i][j] = 1;
    }

    //lower right diagonal
    for (let i = qRow, j = qCol; i < n && j >= 0; i++, j--) {
        if (newBoard[i][j] !== 2)
            newBoard[i][j] = 1;
    }

    newBoard[qRow][qCol] = 2

    return newBoard;
}

function solveNQueen(board, currentColumn = 0) {
    if (currentColumn >= board.length) {
        // Base case: All queens are successfully placed
        return board;
    }

    for (let row = 0; row < board.length; row++) {
        if (board[row][currentColumn] === 0) {
            let newBoard = placeQueen(board, row, currentColumn);

            // Recursively solve for the next column
            const result = solveNQueen(newBoard, currentColumn + 1);
            if (result) {
                // Solution found, return the board
                return result;
            }
        }
    }

    // If no position is valid in this column, return null
    return null;
    // for (leJ
}

printBoard(solveNQueen(nBoard(8)));
