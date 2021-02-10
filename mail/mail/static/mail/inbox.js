document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // Use compose form submit to send the email
  document.querySelector('#compose-form').addEventListener('submit', event => {
    event.preventDefault();
    send_email();
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients='', subject='', body='') {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Fill or clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        const emailEl = document.createElement('div');
        emailEl.classList.add('list-group-item')
        if (email.read) {
          emailEl.classList.add('read');
        }
        emailEl.addEventListener('click', () => load_email(email.id));
        document.querySelector('#emails-view').appendChild(emailEl);

        const senderEl = document.createElement('strong');
        const subjectEl = document.createElement('span');
        const timestampEl = document.createElement('time');

        emailEl.appendChild(senderEl);
        emailEl.appendChild(subjectEl);
        emailEl.appendChild(timestampEl);

        const senderTextNode = document.createTextNode(email.sender);
        const subjectTextNode = document.createTextNode(email.subject);
        const timestampTextNode = document.createTextNode(email.timestamp);

        senderEl.appendChild(senderTextNode);
        subjectEl.appendChild(subjectTextNode);
        timestampEl.appendChild(timestampTextNode);

        const archiveButton = document.createElement('button');
        archiveButton.classList = 'btn btn-sm';
        archiveButton.addEventListener('click', event => {
          event.stopPropagation();
          archive_email(email.id, !email.archived);
        });

        if (mailbox === "inbox") {
          archiveButton.innerHTML = "Archive";
          archiveButton.classList.add('btn-primary');
          emailEl.appendChild(archiveButton);
        } else if (mailbox === "archive") {
          archiveButton.innerHTML = "Unarchive";
          archiveButton.classList.add('btn-secondary');
          emailEl.appendChild(archiveButton);
        }
      });
  });

}

function load_email(id) {
  mark_email_read(id);

  // Show the email view and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  const emailFields = [
    'sender',
    'recipients',
    'subject',
    'timestamp',
    'body'
  ]

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    emailFields.forEach(field => {
      const fieldElement = document.querySelector(`#email-${field}`);
      fieldElement.innerHTML = '';

      const fieldTextNode = document.createTextNode(email[field]);
      fieldElement.appendChild(fieldTextNode);
    });

    document.querySelector('#reply-button').addEventListener('click', () => compose_reply(email));
  });
}

function send_email() {

  // Get recipients, subject and body of an email form compose form input fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a POST request to API to send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients,
        subject,
        body
    })
  })
  .then(response => response.json())
  .then(result => {
      // If the email was successfully sent, load the sent mailbox
      if (result.message) {
        load_mailbox('sent');
      // Else alert the user with error message from API
      } else {
        alert(result.error);
      }
  });
}

function compose_reply(email) {
  const recipients = email.sender;
  const subject = /^Re:/.test(email.subject) ? email.subject : `Re: ${email.subject}`;
  const body = `On ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`
  compose_email(recipients, subject, body);
}

function archive_email(id, archived) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived
    })
  })
  .then(() => load_mailbox("inbox"));
}

function mark_email_read(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}