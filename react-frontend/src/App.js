import React from "react";
import "./App.css";
class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      pn: "",
      un: ""

    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();
    const data = new FormData();
    data.append("file", this.uploadInput.files[0]);

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: data
    })
      .then(res => {
        return res.json();
      })
      .then(data => {
        console.log(data);
        this.setState({ pn: data.pn,
          un: data.un
         });
      });
  }
  render() {
    return (
      <div className="app">
        <form onSubmit={this.handleUploadImage}>
          <div>
            <input
              ref={ref => {
                this.uploadInput = ref;
              }}
              type="file"
            />
          </div>
          <br />
          <div>
            <button type="submit">Upload</button>
          </div>
        </form>
        <h1>{this.state.pn} {this.state.un}</h1>
      </div>
    );
  }
}

export default App;
