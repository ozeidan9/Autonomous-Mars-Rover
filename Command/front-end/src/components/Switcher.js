import React, { useState } from 'react';
import Auto from "./AutoSwitch";

function Switcher() {
  const [value, setValue] = useState(false);
  return (
    <div>
      <Auto
        isOn={value}
        onColor="#FFCC00"
        handleToggle={() => setValue(!value)}
      />
    </div>
  );
}

export default Switcher;