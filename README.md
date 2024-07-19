# mArch

This toolbox provides a multivariate extension to the univariate `arch` toolbox
- https://pypi.org/project/arch/
- https://github.com/bashtage/arch
- https://bashtage.github.io/arch/    

This enables the estimation of the following multivariate ARCH specifications:
- The Constant Conditional Correlation model (Bollerslev 1990)
- The Dynamic Conditional Correlation (1,1) model (Engle 2002)
- The Asymmetric Dynamic Conditional Correlation (1,1) model (Cappiello et.
 al. 2006)

## Requirements and Installation

The main toolbox dependency is the `arch` toolbox, version 5. It has not been tested on version 6 for compatibility, this is for future development. Additional packages required are `numpy`, `pandas`, `scipy` and `statsmodels`, which are all already dependencies of `arch`.

There is no distributable package yet, the functionality can be obtained by placing a copy of the `mArch` file in the relevant directory.

## Functionality

This section details the basic functionality of the toolbox. The github repo also provides a demonstration example, both as a python script (`mArch_demo.py`) and as a jupyter notebook (`mArch_demo.ipynb`). The `mArch` class contains all the functionality required  and is imported as follows.

```python
from mArch import mArch
```

### Initialisation

An empty multivariate GARRCH estimation object is initialised using the empirical data set:

```python
mArchEst = mArch(myDataFrame)
```
Importantly, as is the case for the `arch` toolbox, an entire dataset can be loaded and later split into estimation/forecasting portions using the `first_obs`/`last_obs` syntax.

### Configuring the univariate and multivariate processes

Next, the estimation is configured by specifying:
- The univariate process required to model the individual series volatilities
- The multivariate process used to model the correlations across series
- The distribution used for the innovations.

This is done as follows:
```python
from arch import EGARCH

univarSpec = EGARCH(p = 2, q = 2, o = 1)
mArchEst.setArch(univarSpec,
                 errors = 'Student',
                 multivar = 'dcca')
```

EGARCH is used as an example here, however the toolbox will accept all the individual volatility processes present in the `arch` toolbox. These simply need to be imported first. The toolbox has four multivariate specifications:
- `'naive'`: this models the correlation matrix using the identity matrix, essentially treating the series as independent. This can be useful for running batch univariate estimations.
- `'ccc'`: This implements the Constant Conditional Correlation model of Bollerslev (1990)
- `'dcc'`: This implements the Dynamic Conditional Correlation model of Engle (2002)
- `'dcca'`: This implements the Asymmetric Dynamic Conditional Correlation of Cappiello et.
 al. (2006)

Two options are available for the distribution of innovations:
- `'Normal'` for standard normal innovations
 - `'Student'` for Student's t innovations

### Estimating the multivariate GARCH

The estimation itself is run using the same syntax as for univariate estimations in the standard `arch` toolbox, for instance:

```python
initVals = [0.05, 0.9, 0.05 ,7]     # Initial values for DCCA parameters
mArchEst.fit(update_freq = 0,       # Don't display ML estimation iterations
             last_obs = split_date, # Pick an observation in the dataset to end estimation
             init = initVals)
```

The only additional parameter here is `initVals`, which provides initialisation values for the DCC and DCCA specifications. The toolbox provides defaults, but these can be overridden as shown here.

Once the estimation is terminated, a summary can be displayed using:
```python
mArchEst.summary()
```

The `mArchEst` object saves the `arch` estimation result class for each univariate model (an instance of `ARCHModelResult`) in a list that can be accesses via `mArchEst.archResults`, while the results of the multivariate correlation estimation stage are saved in a `dict` stored in `mArchEst.multivarResults`. A full list of stored results and properties can be found in the function help for `mArch`.

### Forecasting

The `mArch` toolbox also provides multivariate forecasting, again using a similar syntax to the univariate `arch` toolbox. In the example below, we generate a 5-period ahead forecast from the end of the estimation period, using the simulation method.

```python
forecastMethod = 'simulation'
Sigma_t_Predicted = mArchEst.forecast(horizon = 5,
                                  start = split_date,
                                  method = forecastMethod)
```

## References:
- Bollerslev, T., 1990. Modelling the coherence in short-run nominal exchange rates: a multivariate generalized ARCH model. *The Review of Economics and Statistics*, pp.498-505.
- Cappiello, L., Engle, R.F. and Sheppard, K., 2006. Asymmetric dynamics in the correlations of global equity and bond returns. *Journal of Financial Econometrics*, 4(4), pp.537-572.
- Engle, R., 2002. Dynamic conditional correlation: A simple class of multivariate generalized autoregressive conditional heteroskedasticity models. *Journal of Business & Economic Statistics*, 20(3), pp.339-350.
