module port_test (port1, port3, port5, port7, port9, port11, port13, led0, led1, led2, led3, led4, led5, led6);

	input port1, port3, port5, port7, port9, port11, port13;
	
	output led0, led1, led2, led3, led4, led5, led6;
	
	assign led0 = port1;
	assign led1 = port3;
	assign led2 = port5;
	assign led3 = port7;
	assign led4 = port9;
	assign led5 = port11;
	assign led6 = port13;

endmodule
