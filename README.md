# books

A Python program for scanning ISBNs (barcodes) to check if a book is already listed in our webshop. 
Based on the inventory balance, the script makes a recommendation, whether to sell the book in webshop or physical store. 
A price history is also provided for the book.

<i>This is the second iteration of the script, with added features and optimized iteration algorithm.</i> 
You can check out the earlier version <a href="https://github.com/EskoJanatuinen/isbn_search/" target="_blank">here</a>.

Main.py runs the program. 

Updates listed online products to a local SQLite database daily. Scanned ISBN-barcodes are compared to this list. 
Allows scanning even if the database cannot be updated.

</br>
</br>

<img width="238" alt="Screenshot 2022-08-15 at 16 40 56" src="https://user-images.githubusercontent.com/47399693/184647390-03c4129a-e5d3-43b9-9cbf-457fbc02f5b9.png">
