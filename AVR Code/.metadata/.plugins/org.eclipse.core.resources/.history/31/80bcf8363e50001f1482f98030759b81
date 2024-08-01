 /******************************************************************************
 * 																			   *
 * 					Author: Abdelrhman Khaled Sobhi			     			   *
 *																			   *
 * 								Group : 79								       *
 *																			   *
 *******************************************************************************/

#ifndef UART_H_
#define UART_H_

#include "std_types.h"

/*******************************************************************************
 | 							Structures and Enumerators			   		       |
 *******************************************************************************/

typedef enum{
	Frame_5_bit,Frame_6_bit,Frame_7_bit,Frame_8_bit,Frame_9_bit = 7
}UART_BitData;

typedef enum{
	Parity_Disable,Parity_Enable_Even= 2,Parity_Enable_Odd
}UART_Parity;

typedef enum{
	Stop_1_bit,Stop_2_bit
}UART_StopBit;

typedef enum{
	Buad_Rate_10     = 10,
	Buad_Rate_300    = 300,
	Buad_Rate_600    = 600,
	Buad_Rate_1200   = 1200,
	Buad_Rate_2400   = 2400,
	Buad_Rate_4800   = 4800,
	Buad_Rate_9600   = 9600,
	Buad_Rate_14400  = 14400,
	Buad_Rate_19200  = 19200,
	Buad_Rate_38400  = 38400,
	Buad_Rate_57600  = 57600,
	Buad_Rate_115200 = 115200,
	Buad_Rate_128000 = 128000,
	Buad_Rate_256000 = 256000
}UART_BaudRate;

typedef struct{
	 UART_BitData bit_data;
	 UART_Parity parity;
	 UART_StopBit stop_bit;
	 UART_BaudRate baud_rate;
}UART_ConfigType;

/*******************************************************************************
 | 									Functions			   		               |
 *******************************************************************************/

void UART_init(const UART_ConfigType *Config_Ptr);

void UART_sendByte(const uint8 data);

uint8 UART_recieveByte(void);

void UART_sendString(const uint8 *Str);

void UART_receiveString(uint8 *Str);

#endif
