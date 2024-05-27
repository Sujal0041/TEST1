import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
} from 'react-native';
import AntDesign from 'react-native-vector-icons/AntDesign';
import {useNavigation} from '@react-navigation/native';

const AccountSettings = () => {
  const navigation = useNavigation();
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSaveChanges = () => {
    // Logic to save changes goes here
    console.log('Changes saved');
  };

  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.container}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}>
          <AntDesign name="arrowleft" size={24} color="white" />
        </TouchableOpacity>

        <Text style={styles.title}>Account Settings</Text>
        <View style={styles.formContainer}>
          <View style={styles.inputContainer}>
            <Text style={styles.heading}>Username</Text>
            <TextInput
              style={[styles.input, {color: '#ffffff'}]}
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
              placeholder="Enter your username"
              placeholderTextColor="#aaaaaa"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.heading}>Phone Number</Text>
            <TextInput
              style={[styles.input, {color: '#ffffff'}]}
              value={phoneNumber}
              onChangeText={setPhoneNumber}
              keyboardType="phone-pad"
              placeholder="Enter your phone number"
              placeholderTextColor="#aaaaaa"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.heading}>Password</Text>
            <TextInput
              style={[styles.input, {color: '#ffffff'}]}
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              placeholder="Enter your password"
              placeholderTextColor="#aaaaaa"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.heading}>Confirm Password</Text>
            <TextInput
              style={[styles.input, {color: '#ffffff'}]}
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
              placeholder="Confirm your password"
              placeholderTextColor="#aaaaaa"
            />
          </View>

          <TouchableOpacity
            style={styles.saveButton}
            onPress={handleSaveChanges}>
            <Text style={styles.saveButtonText}>Save Changes</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1c1e1f',
    padding: 20,
  },
  container: {
    width: '100%',
    alignItems: 'center',
  },
  backButton: {
    alignSelf: 'flex-start',
    marginBottom: 20,
    position: 'relative',
    bottom: 25,
  },
  title: {
    color: '#ffffff',
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    position: 'relative',
    bottom: 75,
  },
  heading: {
    color: '#ffffff',
    fontSize: 16,
    marginBottom: 5,
    marginLeft: 10,
  },
  inputContainer: {
    width: '100%',
    marginBottom: 20,
  },
  input: {
    height: 50,
    borderBottomWidth: 1,
    borderColor: '#3c8dbc',
    paddingHorizontal: 10,
    fontSize: 16,
    color: '#ffffff',
    borderRadius: 5,
    backgroundColor: '#2c2c2e',
  },
  saveButton: {
    backgroundColor: '#3c8dbc',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 25,
    marginTop: 30,
  },
  formContainer: {
    position: 'relative',
    bottom: 55,
    width: '100%',
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default AccountSettings;
