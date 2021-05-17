module input_test (number, number0, number1, number2, number3, number4);

	input [4:0]number;
	
	output number0, number1, number2, number3, number4;

	assign number0 = number[0];
	assign number1 = number[1];
	assign number2 = number[2];
	assign number3 = number[3];
	assign number4 = number[4];

endmodule
