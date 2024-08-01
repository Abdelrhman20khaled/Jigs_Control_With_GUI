 /******************************************************************************
 * 																			   *
 * 					Author: Abdelrhman Khaled Sobhi			     			   *
 *																			   *
 * 								Group : 79								       *
 *																			   *
 *******************************************************************************/

#include "uart.h"
#include "avr/io.h"
#include "common_macros.h"

/*******************************************************************************
 | 							   		Functions			          		       |
 *******************************************************************************/

/*
 * Description :
 *
 *	1- Set up uART to work with double speed (U2X).
 *	2- Enable TXEN and RXEN.
 *	3- Check about the bit of data 9 bit or no.
 *  4- Modify the Baud Rate equation.
 *	5- setup the UBRRH and UBRRL values.
 *
 */

void UART_init(const UART_ConfigType *Config_Ptr){

	uint16 ubrr_value=0;

	UCSRA = (1<< U2X);

	UCSRB = (1<<RXEN) | (1<<TXEN);

	/*
	 * This check is important for determine the number of bits in the data frame
	 * if number of bits less than 9 bit the 2 bits UCSZ0 and UCSZ1 in register
	 * UCSRC will set to 1, but if the number of bits equal to 9 bits the 2 bits
	 * UCSZ0 and UCSZ1 in register UCSRC will set to 1 and the bit UCSZ2 in register
	 * UCSZ2 will set to 1 else, so this if important for configuration.
	 */

	if(Config_Ptr->bit_data == Frame_9_bit){

		UCSRC = (1<<URSEL) | ((Config_Ptr->parity & 0x03)<<4)
					 | ((Config_Ptr->stop_bit & 0x01)<<3)
					 | ((Config_Ptr->bit_data & 0X03)<<1);

		UCSRB |= (1<< UCSZ2);

	}
	else{
		UCSRC = (1<<URSEL) | ((Config_Ptr->parity & 0x03)<<4)
							 | ((Config_Ptr->stop_bit & 0x01)<<3)
							 | ((Config_Ptr->bit_data & 0X03)<<1);
	}

	ubrr_value = (uint16)(((F_CPU / (Config_Ptr->baud_rate * 8UL))) - 1);

	UBRRH = ubrr_value >>8;
	UBRRL = ubrr_value;
}

void UART_sendByte(const uint8 data)
{
	/*
	 * UDRE flag is set when the Tx buffer (UDR) is empty and ready for
	 * transmitting a new byte so wait until this flag is set to one
	 */
	while(BIT_IS_CLEAR(UCSRA,UDRE)){}

	/*
	 * Put the required data in the UDR register and it also clear the UDRE flag as
	 * the UDR register is not empty now
	 */
	UDR = data;

	/************************* Another Method *************************
	UDR = data;
	while(BIT_IS_CLEAR(UCSRA,TXC)){} // Wait until the transmission is complete TXC = 1
	SET_BIT(UCSRA,TXC); // Clear the TXC flag
	 *******************************************************************/
}

/*
 * Description :
 * Functional responsible for receive byte from another UART device.
 */
uint8 UART_recieveByte(void)
{
	/* RXC flag is set when the UART receive data so wait until this flag is set to one */
	while(BIT_IS_CLEAR(UCSRA,RXC)){}

	/*
	 * Read the received data from the Rx buffer (UDR)
	 * The RXC flag will be cleared after read the data
	 */
	return UDR;
}

/*
 * Description :
 * Send the required string through UART to the other UART device.
 */
void UART_sendString(const uint8 *Str)
{
	uint8 i = 0;

	/* Send the whole string */
	while(Str[i] != '\0')
	{
		UART_sendByte(Str[i]);
		i++;
	}
	/************************* Another Method *************************
	while(*Str != '\0')
	{
		UART_sendByte(*Str);
		Str++;
	}
	 *******************************************************************/
}

/*
 * Description :
 * Receive the required string until the '#' symbol through UART from the other UART device.
 */
void UART_receiveString(uint8 *Str)
{
	uint8 i = 0;

	/* Receive the first byte */
	Str[i] = UART_recieveByte();

	/* Receive the whole string until the '#' */
	while(Str[i] != '#')
	{
		i++;
		Str[i] = UART_recieveByte();
	}

	/* After receiving the whole string plus the '#', replace the '#' with '\0' */
	Str[i] = '\0';
}
