module decoder (number, control, button0, button1, button2, button3, switch17, switch16, switch15);

	input [2:0]number;
	input control;
	
	output reg button3, button2, button1, button0;
	output reg switch17, switch16, switch15;
	
	always @ (posedge control)
	begin
		button3 <= button3;
		button2 <= button2;
		button1 <= button1;
		button0 <= button0;
		switch17 <= switch17;
		switch16 <= switch16;
		switch15 <= switch15;
		case(number)
			4'b0000: button3  <= ~button3 ;
			4'b0001: button2  <= ~button2 ;
			4'b0010: button1  <= ~button1 ;
			4'b0011: button0  <= ~button0 ;
			4'b0100: switch17 <= ~switch17;
			4'b0101: switch16 <= ~switch16;
			4'b0110: switch15 <= ~switch15;
			default: begin
				button3 <= 1'b1;
				button2 <= 1'b1;
				button1 <= 1'b1;
				button0 <= 1'b1;
				switch17 <= 1'b0;
				switch16 <= 1'b0;
				switch15 <= 1'b0;
			end
		endcase
	end
	
endmodule
