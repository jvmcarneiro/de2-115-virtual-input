module decoder (number, control, button3, button2, button1, button0, switch17, switch16, switch15, switch14, switch13, switch12, switch11, switch10, switch9, switch8, switch7, switch6, switch5, switch4, switch3, switch2, switch1, switch0);

	input [4:0] number;
	input control;
	output button3, button2, button1, button0, switch17, switch16, switch15, switch14, switch13, switch12, 
	switch11, switch10, switch9, switch8, switch7, switch6, switch5, switch4, 
	switch3, switch2, switch1, switch0;
	
	reg [31:0] switch_control;
	reg [31:0] reset;
	
	switch button3_block(
		.switch_enable(switch_control[0]),
		.reset(reset[0]),
		.data_out(button3)
		);
		
	switch button2_block(
		.switch_enable(switch_control[1]),
		.reset(reset[1]),
		.data_out(button2)
		);
		
	switch button1_block(
		.switch_enable(switch_control[2]),
		.reset(reset[2]),
		.data_out(button1)
		);
		
	switch button0_block(
		.switch_enable(switch_control[3]),
		.reset(reset[3]),
		.data_out(button0)
		);
		
	switch switch17_block(
		.switch_enable(switch_control[4]),
		.reset(reset[4]),
		.data_out(switch17)
		);
		
	switch switch16_block(
		.switch_enable(switch_control[5]),
		.reset(reset[5]),
		.data_out(switch16)
		);
		
	switch switch15_block(
		.switch_enable(switch_control[6]),
		.reset(reset[6]),
		.data_out(switch15)
		);
		
	switch switch14_block(
		.switch_enable(switch_control[7]),
		.reset(reset[7]),
		.data_out(switch14)
		);
		
	switch switch13_block(
		.switch_enable(switch_control[8]),
		.reset(reset[8]),
		.data_out(switch13)
		);
		
	switch switch12_block(
		.switch_enable(switch_control[9]),
		.reset(reset[9]),
		.data_out(switch12)
		);
		
	switch switch11_block(
		.switch_enable(switch_control[10]),
		.reset(reset[10]),
		.data_out(switch11)
		);
		
	switch switch10_block(
		.switch_enable(switch_control[11]),
		.reset(reset[11]),
		.data_out(switch10)
		);
	
	switch switch9_block(
		.switch_enable(switch_control[12]),
		.reset(reset[12]),
		.data_out(switch9)
		);
		
	switch switch8_block(
		.switch_enable(switch_control[13]),
		.reset(reset[13]),
		.data_out(switch8)
		);
		
	switch switch7_block(
		.switch_enable(switch_control[14]),
		.reset(reset[14]),
		.data_out(switch7)
		);
		
	switch switch6_block(
		.switch_enable(switch_control[15]),
		.reset(reset[15]),
		.data_out(switch6)
		);
	
	switch switch5_block(
		.switch_enable(switch_control[16]),
		.reset(reset[16]),
		.data_out(switch5)
		);
	
	switch switch4_block(
		.switch_enable(switch_control[17]),
		.reset(reset[17]),
		.data_out(switch4)
		);
	
	switch switch3_block(
		.switch_enable(switch_control[18]),
		.reset(reset[18]),
		.data_out(switch3)
		);
	
	switch switch2_block(
		.switch_enable(switch_control[19]),
		.reset(reset[19]),
		.data_out(switch2)
		);
	
	switch switch1_block(
		.switch_enable(switch_control[20]),
		.reset(reset[20]),
		.data_out(switch1)
		);
	
	switch switch0_block(
		.switch_enable(switch_control[21]),
		.reset(reset[21]),
		.data_out(switch0)
		);

	always @ (control)
	begin
		if (control)
		begin
			switch_control = 'h00000000;
			switch_control[number] = 1;
			if (number > 21) 
			begin
				reset = 'hFFFFFFFF;
				switch_control = 'hFFFFFFFF;
			end
		end
		else
		begin
			switch_control = 'h00000000;
			reset = 'h00000000;
		end
	end
	
	
endmodule
