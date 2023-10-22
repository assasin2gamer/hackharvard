import './App.css';
import './index.css';
import React, {useState, useEffect} from "react";




function App() {

  
  const [letter, setLetter] = useState([]);
  const [choices, setChoices] = useState([]);
  const[loop, setLoop] = useState(0)
  const [count, setCount] = useState(0);

  let choice = []
  const[alphabet, setAlphabet] = useState( [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
  ]);
  const [dict, setDict]= useState([
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z', '-'
  ]);

  

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCount((prevCount) => prevCount + 1);
      
    }, 1000);
    const appendToLetters = (newItem) => {
      setLetter((prevChoices) => [...prevChoices, newItem]);
    };

    const resetIntervalId = setInterval(() => {
      setCount(0);
      setSpacebarCount(0);
      if (spacebarCount == 1){
        appendToChoices(0)
        choiceAction(1)
      }
      else if(spacebarCount == 3){
        appendToLetters("-")
        setChoices([])
      }
      else{
        appendToChoices(1)
        choiceAction(0)
      }
      setLoop(loop+1)
    }, 3000);

    return () => {
      clearInterval(intervalId);
      clearInterval(resetIntervalId);
    };
  }, [choices, letter, dict]);

  const [spacebarCount, setSpacebarCount] = useState(0);
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === ' ' || e.keyCode === 32) {
        // Increment the count when the spacebar is pressed
        setSpacebarCount(spacebarCount + 1);
      }
    };

    // Add the event listener when the component mounts
    window.addEventListener('keydown', handleKeyDown);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [spacebarCount]); // Include spacebarCount in the dependency array


  const appendToChoices = (newItem) => {
    setChoices((prevChoices) => [...prevChoices, newItem]);
  };
  const appendToLetters = (newItem) => {
    setLetter((prevChoices) => [...prevChoices, newItem]);
  };
  
  const choiceAction = (num) => {
    console.log('choiceaction')
    if (num == 1) {
      setDict(dict.slice(0, dict.length / 2)); // Get the first half
      console.log('1')
    } else {
      setDict(dict.slice(dict.length / 2)); // Get the last half
      console.log('0')
    }
    if (dict.length == 1)
    {
      appendToLetters(dict)
      setDict(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
      'U', 'V', 'W', 'X', 'Y', 'Z', '-', '<'])
    }
    
    setAlphabet(dict)
    
    
  }
    
  





 





  return (
    <div className="App">
    <div style={{fontSize:'100px', height:'20vh', borderBottom:'solid', width:'80%', margin:'auto'}}>
      {letter}
    </div>
    <div>
      spacebarCount: {spacebarCount}
    </div>

    <div className="alphabet-container">
      <div className="alphabet" style={{height:'20vh'}}>
        {alphabet.map((letter, index) => (
          <span key={index} className={index < alphabet.length / 2 ? 'red-line' : ''}>
            {letter}
          </span>
        ))}
      </div>
    </div>

    <div style={{ margin:'auto', width:'100%'}}>
      <div style={{display:'flex', justifyContent:'center', fontSize:'80px'}}>
        <div style={{width:'90px', color:'red'}}>
          0
        </div>
        <div style={{width:'90px'}}>
          1
        </div>
      </div>
      
    </div>
  </div>
        
  );
}

export default App;