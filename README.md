# fourier
This package contains one class intended for use:
  `FourierAnalyzer`.
When the constructor is called, a GUI will start with
  an interactive visualization related to the fourier transform
  allowing the user to investigate periodicities in
  their data.

# usage
import the python module and call the constructor for `FourierAnalyzer`

```
class FourierAnalyzer:
    
    def __init__(self, x_data=None, y_data=None, min_winding=0.0, max_winding=1.0):
        ...
```
the constructor parameters `x_data` and `y_data` should be 1D python Lists or Numpy arrays
`min_winding` and `max_winding` refer to the range of frequencies you would like to analyze your input data over

# example
```
>>> import fourier_analysis as fa
>>> import numpy as np
>>> t = np.linspace(0.0, 20.0*np.pi, 10000)
>>> fa.FourierAnalyzer(x_data=t, y_data=np.sin(t) + 1.0, min_winding=0.0, max_winding=2)
```
