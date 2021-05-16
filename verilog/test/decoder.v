module decoder (number, control, button3, button2, button1, button0, switch17, switch16, switch15, switch14, switch13, switch12, switch11, switch10, switch9, switch8, switch7, switch6, switch5, switch4, switch3, switch2, switch1, switch0, led_control);

	input [4:0]number;
	input control;
	
	output reg button3, button2, button1, button0;
	output reg switch17, switch16, switch15, switch14, switch13, switch12, switch11, switch10, switch9, switch8, switch7, switch6, switch5, switch4, switch3, switch2, switch1, switch0;
	output led_control;
	

	always @ (negedge control)
	begin
		case(number)
			5'b00000:	button3 <= !button3;
			5'b00001:	button2 <= !button2;
			5'b00010:	button1 <= !button1;
			5'b00011:	button0 <= !button0;
			5'b00100:	switch17 <= !switch17;
			5'b00101:	switch16 <= !switch16;
			5'b00110:	switch15 <= !switch15;
			5'b00111:	switch14 <= !switch14;
			5'b01000:	switch13 <= !switch13;
			5'b01001:	switch12 <= !switch12;
			5'b01010:	switch11 <= !switch11;
			5'b01011:	switch10 <= !switch10;
			5'b01100:	switch9 <= !switch9;
			5'b01101:	switch8 <= !switch8;
			5'b01110:	switch7 <= !switch7;
			5'b01111:	switch6 <= !switch6;
			5'b10000:	switch5 <= !switch5;
			5'b10001:	switch4 <= !switch4;
			5'b10010:	switch3 <= !switch3;
			5'b10011:	switch2 <= !switch2;
			5'b10100:	switch1 <= !switch1;
			5'b10101:	switch0 <= !switch0;
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
				switch5 <= 1'b0;
				switch4 <= 1'b0;
				switch3 <= 1'b0;
				switch2 <= 1'b0;
				switch1 <= 1'b0;
				switch0 <= 1'b0;
			end
		endcase
	end
	
	assign led_control = control;

endmodule
