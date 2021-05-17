module decoder (number, control, led_control, button0, button1, button2, button3, switch17, switch16, switch15, switch14, switch13, switch12, switch11, switch10, switch9, switch8, switch7, switch6, value);

	input [3:0]number;
	input control;
	input value;
	
	output reg button3, button2, button1, button0;
	output reg switch17, switch16, switch15, switch14, switch13, switch12, switch11, switch10, switch9, switch8, switch7, switch6;
	
	output led_control;
	
	always @ (posedge control)
	begin
		button3 <= button3;
		button2 <= button2;
		button1 <= button1;
		button0 <= button0;
		switch17 <= switch17;
		switch16 <= switch16;
		switch15 <= switch15;
		switch14 <= switch14;
		switch13 <= switch13;
		switch12 <= switch12;
		switch11 <= switch11;
		switch10 <= switch10;
		switch9 <= switch9;
		switch8 <= switch8;
		switch7 <= switch7;
		switch6 <= switch6;
		case(number)
			4'b0000: button3  <= ~button3 ;
			4'b0001: button2  <= ~button2 ;
			4'b0010: button1  <= ~button1 ;
			4'b0011: button0  <= ~button0 ;
			4'b0100: switch17 <= ~switch17;
			4'b0101: switch16 <= ~switch16;
			4'b0110: switch15 <= ~switch15;
			4'b0111: switch14 <= ~switch14;
			4'b1000: switch13 <= ~switch13;
			4'b1001: switch12 <= ~switch12;
			4'b1010: switch11 <= ~switch11;
			4'b1011: switch10 <= ~switch10;
			4'b1100: switch9  <= ~switch9 ;
			4'b1101: switch8  <= ~switch8 ;
			4'b1110: switch7  <= ~switch7 ;
			4'b1111: switch6  <= ~switch6 ;
			default: begin
				button3 <= 1'b1;
				button2 <= 1'b1;
				button1 <= 1'b1;
				button0 <= 1'b1;
				switch17 <= 1'b0;
				switch16 <= 1'b0;
				switch15 <= 1'b0;
				switch14 <= 1'b0;
				switch13 <= 1'b0;
				switch12 <= 1'b0;
				switch11 <= 1'b0;
				switch10 <= 1'b0;
				switch9 <= 1'b0;
				switch8 <= 1'b0;
				switch7 <= 1'b0;
				switch6 <= 1'b0;
			end
		endcase
	end
	
	assign led_control = value;

endmodule
