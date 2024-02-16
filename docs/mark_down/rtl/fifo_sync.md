# fifo_sync

The `fifo_sync` module is a parameterized synchronous FIFO (First-In, First-Out) with configurable data width and depth. It also incorporates "almost full" and "almost empty" indicators.

## Parameters

- **DATA_WIDTH**: The width of the data in bits. The default is 4.

- **DEPTH**: The depth of the FIFO, representing how many elements it can store. The default is 4.

- **ALMOST_WR_MARGIN**: Margin to indicate almost full status. The default is 1.

- **ALMOST_RD_MARGIN**: Margin to indicate almost empty status. The default is 1.

- **INSTANCE_NAME**: Name for this particular FIFO instance used for error reporting. The default is "DEADF1F0".

## Ports

- **i_clk**: Clock input for the FIFO.

- **i_rst_n**: Active low reset signal.

- **i_write**: Write enable signal. When high, data can be written to the FIFO.

- **i_wr_data**: Data input to write to the FIFO.

- **ow_wr_full**: Output signal indicating if the FIFO is full.

- **ow_wr_almost_full**: Output signal indicating if the FIFO is almost full.

- **i_read**: Read enable signal. When high, data can be read from the FIFO.

- **ow_rd_data**: Data output from the FIFO.

- **ow_rd_empty**: Output signal indicating if the FIFO is empty.

- **ow_rd_almost_empty**: Output signal indicating if the FIFO is almost empty.

## Internal Design

The FIFO uses an internal memory array to store data and Binary Counters for tracking read and write positions. Binary counters use the parameters provided to size the counters correctly for the depth of the FIFO.

## Behavior

The FIFO stores data when `i_write` is asserted and `ow_wr_full` is not signaled. Data is read when `i_read` is asserted and `ow_rd_empty` is not indicated. "Almost full" and "almost empty" signals provide a margin-based indication for near-full or near-empty conditions suitable for flow control.

## Error Checking

In debug/translational-off blocks, the FIFO reports errors (like write attempts when full or read attempts when empty) along with the instance name for easier debugging. It also includes dumping signals into a `.vcd` file for waveform analysis.

---

[Return to Index](index.md)

----------