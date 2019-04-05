ZSH-Completion
==============

You can install a basic ZSH-Completion from the github repository. Simply
download it and drop it in your ``fpath``:


.. code:: console

    $ wget https://raw.githubusercontent.com/autophagy/faereld/master/zsh-completion/_faereld
    $ fpath+=$PWD
    $ compinit faereld

You will then be able to complete the basic Færeld commands:

.. code:: console

    $ faereld <TAB>
    help          -- Print the help
    insert        -- Insert a time tracking record into Færeld
    productivity  -- Produce a summary of productivity aggregated over hours and days of the week
    projects      -- Produce a summary of time spent on project specific areas
    summary       -- Produce a summary of time spent on all areas
