Very basic integration with one command
## Configure Atom on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for Atom.
3. Click **Add instance** to create and configure a new integration instance.
4. Click **Test** to validate the integration.
## Commands
You can execute these commands from the Demisto CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.
### get-atom
***
A command that returns process args and return an output


#### Base Command

`get-atom`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| orbit | Flag True to Return "Electron" | Required | 
| center | Flag True to Return "Nucleus" | Required | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| hello | String | Should be Hello \*\*something\*\* here | 
| Atom.Orbit | String | Atom's Orbit | 
| Atom.Center | String | Atom's Orbit | 


#### Command Example
```!get-atom orbit="true" center="true"```

#### Context Example
```
{
    "Atom": {
        "Center": "nucleus",
        "Orbit": "electron"
    }
}
```

#### Human Readable Output

>### Results
>|Center|Orbit|
>|---|---|
>| nucleus | electron |

