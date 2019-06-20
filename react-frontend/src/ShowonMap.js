import React,{ Component } from 'react';
import Geocode from 'react-geocode';
import Map from './maps';


class ShowonMap extends Component{

    constructor(){
        super();
        this.state={
            lat:0,
            lng:0,
        };
    }

    render(){
        Geocode.setApiKey('AIzaSyCLXUeNBnr-U_526lUfTfpPFg6Y6h9ogg4');
        Geocode.enableDebug();
        Geocode.fromAddress(this.props.place).then(response => {
            const { lat, lng } = response.results[0].geometry.location;
            this.setState({
                lat:lat,
                lng:lng,
            });
        },error => {
            console.error(error);
        });
        console.log(this.state.lat,this.state.lng)

        return(
            <div className="grid">
                <Map lat={this.state.lat} lng={this.state.lng} />
            </div>
        );
    }
}

export default ShowonMap;