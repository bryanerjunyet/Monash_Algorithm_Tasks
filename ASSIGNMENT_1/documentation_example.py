


###Solution 1 (less efficient): 

def virtual_book_buster(bookcase):

	"""
		Function description: This function returns an output array containing only the unique integers contained within the input array via the use of Merge Sort and Linear Searching. 

		Approach description: Since the titles of the books are integers, we can sort this using Merge Sort. After sorting the books, all of the duplicate titles are next to one another, so then by effectively linear searching through the bookcase (array), we can compare one element to the next and see if it is identical. If it isn't, then we add the first element to the output array, but if it is identical, then we do not add the element to the output array. This repeats until we have finished searching the sorted input array, and the output array will contain only the unique elements from the input array, which we then return. 

		Input: 
			bookcase: an array based list containing integers 
		
		Output: An array based list containing only the unique integers from the input array 
		
		Time complexity: O(n*log(n)), where n is the number of elements in the input array 

		Time complexity analysis : Given n is the number of elements in the input list,
		
			The Merge Sorting section costs O(n*log(n)) best/worst case in time, 

			The effective Linear Searching section costs O(n) best/worst in time, since we're just comparing each element to the next
			O(n*log(n)) + O(n) = O(n*log(n))
			
		Space complexity: O(n),  where n is the number of elements in the input array

		Space complexity analysis: Merge sort and output array both require O(n) aux space O(n) + O(n) = O(n).
		
	"""
	
	output = []
	
	#sort the list using merge sort
	sorted_list = merge_sort(bookcase)  ###note this is not present here but should be in your actual assignments
	
	
	#"linear search" through sorted output comparing elements adding unique ones to output array
	for i in range(len(sorted_list)-1): 
		if sorted_list[i] != sorted_list[i+1]: 
			output.append(sorted_list[i])
		  
	#deal with the corner case of not adding the last element 
	if len(sorted_list) > 0: 
		output.append(sorted_list[-1])
	  
	return output
	

###Solution 2 (more efficient): 

def virtual_book_buster(bookcase):
	"""
		Function description: This function returns an output array containing only the unique integers contained within the input array via the use of a modified Merge Sort to discard duplicates during merging.

		Approach description: Since the titles of the books are integers, we can sort this using Merge Sort. However during the merging process of Merge Sort, if we are ever doing a comparison between two equal integers when choosing which element to place into the merged array first, then we can simply discard one of these integers and place the other in the merged array (and updating pointers appropriately). This means that this modified Merge Sort will not only output a sorted array, but that sorted array will contain only the unique integers contained in the input. This output array is then returned.

		Input: 
			bookcase: an array based list containing integers 
		
		Output: An array based list containing only the unique integers from the input array 
		
		Time complexity: O(n*log(n)), where n is the number of elements in the input array 

		Time complexity analysis : Given n is the number of elements in the input list,
		
			The Merge Sorting section costs O(n*log(n)), as no additional work is being done via the modification to Merge Sort.

		Space complexity: O(n),  where n is the number of elements in the input array

		Space complexity analysis: Merge sort and output array both require O(n) aux space O(n) + O(n) = O(n).
		
	"""
	
		
	#perform modified Merge Sort 
	output = modified_merge_sort(bookcase) 
	
	return output
	

def modified_merge_sort(input_array): 

	"""
	Function description: This function returns a sorted output array containing only the unique integers contained within the input array. 
	
	Input: 
		input_array: an array based list containing integers 
		
	Output: An array based list containing only the unique integers from the input array 
		
	Time complexity: O(n*log(n)), where n is the number of elements in the input array 

	Time complexity analysis :  Given n is the number of elements in the input list,
	
		The Merge Sorting section costs O(n*log(n)), as no additional work is being done via the modification to Merge Sort.

	Space complexity: O(n),  where n is the number of elements in the input array

	Space complexity analysis:  Merge sort and output array both require O(n) aux space O(n) + O(n) = O(n).
	"""
	
	### insert code here
	return output
		
	
	