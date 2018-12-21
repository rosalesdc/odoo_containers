$(document).ready(function(){
	$('.supplier').click(function(){
		var supplier = ($(this).attr('class').split("_")[1]);
		$('.supplier_product_'+supplier).prop('checked', this.checked);
	});


	$('.confirm_order').click(function(){
		var anyBoxesChecked = false;
		$('#purchase_comparision_from input[type="radio"]').each(function() {
	        if ($(this).is(":checked")) {
	            anyBoxesChecked = true;
	        }
	    });
	 
	    if (anyBoxesChecked == false) {
	      alert('Please select at least one product');
	      return false;
	    } 
	});
});
