module switch(switch_enable, reset, data_out);

	input switch_enable;
	input reset;
	
	output reg data_out;
	
	reg data;
	
	always @ (posedge switch_enable)
	begin
		if (reset) data_out <= 1'b0;
		else data_out <= ~data_out;
	end

endmodule