import pandas as pd

class Amortizer:
    """
    *Amortizer* Class instantiates an new object for a loan ammortization calculations. Attributes are used as initial values for the two 
    implemented methods of payment schedule: **annuity** and classic **straight** amortization.

    **Attributes**:

        *amount (float)*: Loan body (i.e. 100000 or 900.50)

        *period (int)*: Number of months (i.e. 5 years = 60)

        *interest_rate (float)*: Interest rate in percents (i.e. if 9% then 9 without '%' sign. Decimal types: 9.5 are allowed.)

    **Methods**:

        straight_amortization(): Calculates amortization table with straight amortization and returns a dataframe.

        annuity_amortization(): Calculates amortization table with annuity payments and returns a dataframe.

        get_summary(method="annuity"): Calculates amortization dataframe (methods: 'straight' or 'annuity') and returns a dictionary with summary statistics.

        to_html(method="annuity"): Calculates amortization dataframe (methods: 'straight' or 'annuity') and exports results to a string with html markup.

        to_json(method="annuity"): Calculates amortization dataframe (methods: 'straight' or 'annuity') and exports results to a string with JSON object.

        to_csv(path: str, method="annuity"): Calculates amortization dataframe (methods: 'straight' or 'annuity') and exports results to the .csv file.

    """

    def __init__(self, amount: float, period: int, interest_rate: float):

        args = [amount, period, interest_rate]
        for arg in args:
            if type(arg) == str:
                raise TypeError("Arguments must be Integer or Float")

        if period <= 0:
            raise ValueError("Period cannot be less than 0 months")
        if interest_rate > 100 or interest_rate < 0:
            raise ValueError("Interest rate per year cannot be more than 100 or less then 0%")

        self.amount = float(amount)
        self.period = period
        self.interest_rate = float(interest_rate)

    def straight_amortization(self):
        """Calculates amortization table with straight amortization.
        A loan amortized in the classic method comprises a series of payments made between equal time intervals.\n
        Classic amortization means that the borrower will amortize an equal amount each payment period, but the interest will differ in size. \n
        Due to that the interest rate is based on the outstanding debt, the interest paid each payment period is going to decrease the further in to the loan period you get. \n
        Which means that in the beginning of the loan period, the payments will be the biggest and  in the end of the loan period the payments will get smaller and smaller.\n

        Returns:
            DataFrame: Returns pandas DataFrame with calculated values
        """
       
        amortization = self.amount / self.period #constant amortization per month
        prev_rem_debt = self.amount #remaining debt from last period (initial = loan amount)
        interest_rate_period = self.interest_rate / 1200

        df = pd.DataFrame(columns = [
        'Month:Period', 
        'Amortization',
        'Interest expense',
        'Payment',
        'Remaining debt'
        ])
        
        for i in range(0, self.period):    
            
            interest_exp = prev_rem_debt * interest_rate_period
            remaining_debt = prev_rem_debt - amortization
            prev_rem_debt = remaining_debt
            payment_amount = interest_exp + amortization
            new_row = {
                'Month:Period': i + 1,
                'Amortization': amortization,
                'Interest expense': interest_exp,
                'Payment': payment_amount,
                'Remaining debt': prev_rem_debt,
            }
            
            df = df.append(new_row, ignore_index=True)
            df = df.round(2)
            df['Remaining debt'] = df['Remaining debt'].map(lambda x: 0 if x<0 else x )
        
        return df



    def annuity_amortization(self):

        """Calculates amortization table with annuity payments\n
        A loan amortized in the annuity method comprises a series of payments made between equal time intervals. \n
        This amortization type is used to pay an equal amount each payment period. In the beginning of the loan period, \n
        the payments will consist of a bigger part interest and a smaller part amortization.\n
         The further towards the end of the loan period you will come, the bigger part of the payment will be amortization and the smaller part interest.\n

        Returns:
            DataFrame: Returns pandas DataFrame with calculated values
        """

        prev_rem_debt = self.amount #remaining debt from last period (initial = loan amount)
        interest_rate_period = self.interest_rate / 1200

        annuity_payment = self.amount * interest_rate_period / (1 - 1 / (1 + interest_rate_period)**self.period ) #Monthly payment

        df = pd.DataFrame(columns = [
        'Month:Period', 
        'Amortization',
        'Interest expense',
        'Payment',
        'Remaining debt'
        ])
        
        for i in range(0, self.period):    
            
            interest_exp = prev_rem_debt * interest_rate_period
            amortization = annuity_payment - interest_exp
            remaining_debt = prev_rem_debt - amortization
            prev_rem_debt = remaining_debt

            new_row = {
                'Month:Period': i + 1,
                'Amortization': amortization,
                'Interest expense': interest_exp,
                'Payment': annuity_payment,
                'Remaining debt': prev_rem_debt,
            }
            
            df = df.append(new_row, ignore_index=True)
            df = df.round(2)
            df['Remaining debt'] = df['Remaining debt'].map(lambda x: 0 if x<0 else x )

        return df

    def get_summary(self, method="annuity"):
        """Calculates amortization dataframe and returns a dictionary with summary statistics.

        Args:
            method (str, optional): Specify one of the following methods to calculate the amortization table: 'straight' or 'annuity' (default)
        Returns:
            dict: Returns a dictionaty with the following keys: \
                'total_cost' (Total cost of the loan), 'average_interest_exp' (Average interest expense),\
                     'average_monthly_pmt' (Average monthly payment), 'total_interest_exp' (Sum of interest payments)
        """        

        if method == 'straight':
            df = self.straight_amortization()
            average_interest_exp = round(df['Interest expense'].mean(), 2)
            average_monthly_pmt = round(df['Payment'].mean(), 2)
            total_interest_exp = round((df['Interest expense'].sum()), 2)
            total_cost = round((df['Payment'].sum()), 2)
            summary = {
                'total_cost': total_cost, 
                'average_interest_exp': average_interest_exp, 
                'average_monthly_pmt': average_monthly_pmt, 
                'total_interest_exp': total_interest_exp
                }
            return summary
        
        if method == 'annuity':
            df = self.annuity_amortization()
            average_interest_exp = round(df['Interest expense'].mean(), 2)
            average_monthly_pmt = round(df['Payment'].mean(), 2)
            total_interest_exp = round((df['Interest expense'].sum()), 2)
            total_cost = round((df['Payment'].sum()), 2)
            summary = {
                'total_cost': total_cost, 
                'average_interest_exp': average_interest_exp, 
                'average_monthly_pmt': average_monthly_pmt, 
                'total_interest_exp': total_interest_exp
                }
            return summary


    def to_html(self, method="annuity"):
        """Calculates amortization dataframe and exports results to html markup.

        Args:
            method (str, optional): Specify one of the following methods to calculate the amortization table: 'straight' or 'annuity' (default)

        Returns:
            str: Returns calculated amortization table within a string in html/css markup.
        """        

        if method == 'straight':
            df = self.straight_amortization()
            return df.to_html()

        if method == 'annuity':
            df = self.annuity_amortization()
            return df.to_html()

    def to_json(self, method="annuity"):
        """Calculates amortization dataframe and exports results to JSON.

        Args:
            method (str, optional): Specify one of the following methods to calculate the amortization table: 'straight' or 'annuity' (default)

        Returns:
            str: Returns calculated amortization table within a string in JSON format.
        """        

        if method == 'straight':
            df = self.straight_amortization()
            return df.to_json()

        if method == 'annuity':
            df = self.annuity_amortization()
            return df.to_json()
    
    def to_csv(self, path: str, method="annuity"):
        """Calculates amortization dataframe and exports results to .csv file.

        Args:
            path (str): Absolute path to a folder where the script should export [method]_amortization.csv file. For unix '/tmp/' or Windows 'C:/User/Andy/Desktop/' (Only forward slash accepted)
            method (str, optional): Specify one of the following methods to calculate the amortization table: 'straight' or 'annuity' (default)

        Returns:
            print: prints success message after the exported file was recorded on your server/local machine.
        """

        full_path = fr'{path}' + f'{method}_amortization.csv'

        if method == 'straight':
            self.straight_amortization().to_csv(full_path, index = False, header=True)
            return print(f"Data was recorded to {method}_amortization.csv at the following location: {path}")

        if method == 'annuity':
            self.annuity_amortization().to_csv(full_path, index = False, header=True)
            return print(f"Data was recorded to {method}_amortization.csv at the following location: {path}")